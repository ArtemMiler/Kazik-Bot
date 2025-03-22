import random

from Database import get_user_data
from Database.db_creation import update_free_spin, add_balance
from Logic.Settings.validations import *

from .slot_check import SlotCheck
from .slot_spin import SlotSpin
from .win_count import WinCount


class BaseBonus:

    def __init__(self, callback_query, state):
        self._callback_query = callback_query
        self._state = state
        self._total_win = 0
        self._chat_id = self._callback_query.message.chat.id

    @property
    def callback_query(self):
        return self._callback_query

    @property
    def state(self):
        return self._state

    async def initialize(self):
        state_data = await self._state.get_data()
        self._total_win = state_data.get("total_win", 0)

    async def _process_spin(self, my_spin):
        from Bot.print_functions import smooth_bonus_transform

        user_data = await get_user_data(self._chat_id)
        free_spin = user_data.free_spin
        bet = user_data.bet

        check = SlotCheck(my_spin.slot)
        free_spin -= 1
        await update_free_spin(self._chat_id, free_spin)
        await smooth_bonus_transform(my_spin.slot, self._callback_query, self._chat_id)
        free_spin += check.count_bonus()
        await update_free_spin(self._chat_id, free_spin)
        check.check_win()
        my_win = WinCount(bet)
        my_win.count_win(check)
        return my_win, check

    async def _count_spin(self, count_func, check):
        from Bot.print_functions import format_message_check

        text = await format_message_check(check, self._chat_id, await count_func())
        return await self._endgame(text)

    async def _endgame(self, text):
        from Bot.Keyboards.all_keyboards import bonus_keyboard, next_keyboard
        from Bot.print_functions import edit

        user_data = await get_user_data(self._chat_id)
        free_spin = user_data.free_spin

        if free_spin <= 0:
            await edit(text, next_keyboard, self._callback_query.message)
            if self._total_win > 0:
                await self._callback_query.answer(f"Поздравляем! Вы выиграли {self._total_win}!",
                                                 show_alert=True)
            await self._state.update_data(temp_win=0, total_win=0, wild_slot=None)
            self._coordinate = None
        else:
            await edit(text, bonus_keyboard, self._callback_query.message)
        return free_spin


class Bonus(BaseBonus):

    def __init__(self, callback_query, state):
        super().__init__(callback_query, state)
        self._temp_win = 0

    async def initialize(self):
        await super().initialize()
        state_data = await self._state.get_data()
        self._temp_win = state_data.get("temp_win", 0)

    async def play_bonus(self):
        my_spin = SlotSpin()
        my_win, check = await self._process_spin(my_spin)
        return await self._count_spin(lambda: self._count_logic(my_win, check), check)

    async def _count_logic(self, my_win, check):
        new_win = my_win.count_win(check)
        self._temp_win = max(self._temp_win, new_win)
        self._total_win += self._temp_win
        await self._state.update_data(temp_win=self._temp_win, total_win=self._total_win)
        await add_balance(self._chat_id, self._temp_win)
        return self._temp_win


class SuperBonus(BaseBonus):

    def __init__(self, callback_query, state):
        super().__init__(callback_query, state)

    async def initialize(self):
        await super().initialize()

    @staticmethod
    def _random_value(ranges):
        random_value = random.uniform(0, 10)
        return next(value for start, end, value in ranges if start <= random_value <= end)

    async def play_bonus(self):
        my_spin = self._generate_super_bonus_spin()
        my_win, check = await self._process_spin(my_spin)
        return await self._count_spin(lambda: self._count_logic(my_win), check)

    def _generate_super_bonus_spin(self):
        my_spin = SlotSpin()
        quantity = self._random_value(QUANTITY_RANGES)
        for _ in range(quantity):
            position = self._random_value(POSITION_RANGES)
            for row in range(ROWS):
                my_spin.slot[row][position] = Sym.get("WILD").get("emoji")
        return my_spin

    async def _count_logic(self, my_win):
        self._total_win += my_win.total_win
        await self._state.update_data(total_win=self._total_win)
        await add_balance(self._chat_id, self._total_win)
        return my_win.total_win


class MegaBonus(BaseBonus):

    def __init__(self, callback_query, state):
        super().__init__(callback_query, state)
        self.wild_slot = set()

    async def initialize(self):
        await super().initialize()
        state_data = await self._state.get_data()
        self.wild_slot = state_data.get("wild_slot", set())

    async def play_bonus(self):
        my_spin = SlotSpin(self.wild_slot)
        my_spin.coordinate_update()
        my_win, check = await self._process_spin(my_spin)
        return await self._count_spin(lambda: self._count_logic(my_win, my_spin), check)

    async def _count_logic(self, my_win, my_spin):
        self._total_win += my_win.total_win
        await self._state.update_data(wild_slot=my_spin.coordinate, total_win=self._total_win)
        await add_balance(self._chat_id, self._total_win)
        return my_win.total_win