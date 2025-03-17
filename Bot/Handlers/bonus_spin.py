from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from Logic import BET, BaseBonus, SlotCheck
from Logic.Settings import BONUS_CONDITIONALS

from .. import format_message_matrix
from ..additional_functoins import play_bonus_game
from ..Keyboards import bonus_keyboard, game_keyboard, select_bonus
from ..print_functions import edit

router = Router()


class BonusGameFSM(StatesGroup):
    bonus_type = State()
    free_spins = State()
    temp_win = State()
    total_win = State()
    wild_slot = State()


bonus_map = {"bonus": 0, "super": 1, "mega": 2}


@router.callback_query(lambda callback: callback.data == "button_buy")
async def button_buy(callback_query: types.CallbackQuery, state: FSMContext):
    user_state = await state.get_data()
    current_bet = user_state.get("bet", BET)
    select_bonus_keyboard = await select_bonus(current_bet)
    await callback_query.message.edit_text("Какую бонусную игру желаете купить?",
                                           reply_markup=select_bonus_keyboard)


@router.callback_query(lambda callback: callback.data in ["back", "next", "cancel"])
async def button_back(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(free_spins=-1)
    await _update_game_screen(callback_query, state, game_keyboard)


@router.callback_query(lambda callback: callback.data in bonus_map)
async def bonus_select(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer("Поздравляем с покупкой бонусной игры 🤑", show_alert=True)

    bonus_type = bonus_map.get(callback_query.data, 0)
    free_spins = BONUS_CONDITIONALS.get(bonus_type, 5)
    await state.update_data(bonus_type=bonus_type, free_spins=free_spins)
    await _update_game_screen(callback_query, state, bonus_keyboard)


@router.callback_query(lambda callback: callback.data == "bonus_spin")
async def bonus_spin(callback_query: types.CallbackQuery, state: FSMContext):
    bonus = BaseBonus(callback_query, state)
    await bonus.initialize()
    await play_bonus_game(bonus, state)


async def _update_game_screen(callback_query, state, keyboard):
    check = SlotCheck()
    text = await format_message_matrix(check.win_slot, state)
    await edit(text, keyboard, callback_query.message)
    await callback_query.answer()
