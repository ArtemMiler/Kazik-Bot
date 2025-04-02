from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from Database import get_user_data
from Database.db_creation import add_balance, update_free_spin
from Logic import BaseBonus, SlotCheck
from Logic.Settings import *

from .. import format_message_matrix
from ..additional_functoins import play_bonus_game
from ..Keyboards import bonus_keyboard, game_keyboard, select_bonus
from ..print_functions import edit

router = Router()


class BonusGameFSM(StatesGroup):
    bonus_type = State()
    temp_win = State()
    total_win = State()
    wild_slot = State()


bonus_map = {
    "bonus": 0,
    "super": 1,
    "mega": 2
}
price_map = {
    0: BONUS_PRISE,
    1: SUPER_BONUS_PRISE,
    2: MEGA_BONUS_PRISE
}


@router.callback_query(lambda callback: callback.data == "button_buy")
async def button_buy(callback_query: types.CallbackQuery):
    user_data = await get_user_data(callback_query.message.chat.id)
    bet = user_data.bet
    select_bonus_keyboard = await select_bonus(bet)
    await callback_query.message.edit_text("Какую бонусную игру желаете купить?",
                                           reply_markup=select_bonus_keyboard)


@router.callback_query(lambda callback: callback.data in ["back", "next", "cancel"])
async def button_back(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(temp_win=0, total_win=0, wild_slot=None)
    await update_free_spin(callback_query.message.chat.id, -1)
    await _update_game_screen(callback_query, game_keyboard)


@router.callback_query(lambda callback: callback.data in bonus_map)
async def bonus_select(callback_query: types.CallbackQuery, state: FSMContext):
    bonus_type = bonus_map.get(callback_query.data, 0)
    free_spins = BONUS_CONDITIONALS.get(bonus_type, 5)
    await state.update_data(bonus_type=bonus_type)
    await update_free_spin(callback_query.message.chat.id, free_spins)

    user_data = await get_user_data(callback_query.message.chat.id)
    bonus_price = user_data.bet * price_map.get(bonus_type, BONUS_PRISE)

    if bonus_price <= user_data.balance:
        await callback_query.answer("Поздравляем с покупкой бонусной игры 🤑",
                                    show_alert=True)
        await add_balance(callback_query.message.chat.id, -bonus_price)
        await _update_game_screen(callback_query, bonus_keyboard)
    elif user_data.balance < MIN_BET:
        await callback_query.answer("Не достаточно средств на Балансе! "
                                    "Ожидайте пополнение счета завтра",
                                    show_alert=True)
    else:
        await callback_query.answer("Недостаточно средств для покупки бонуса! "
                                    "Попробуйте уменьшить ставку или купить бонус дешевле",
                                    show_alert=True)


@router.callback_query(lambda callback: callback.data == "bonus_spin")
async def bonus_spin(callback_query: types.CallbackQuery, state: FSMContext):
    bonus = BaseBonus(callback_query, state)
    await bonus.initialize()
    await play_bonus_game(bonus, state)


async def _update_game_screen(callback_query, keyboard):
    check = SlotCheck()
    text = await format_message_matrix(check.win_slot, callback_query.message.chat.id)
    await edit(text, keyboard, callback_query.message)
    await callback_query.answer()
