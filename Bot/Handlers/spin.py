from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from Database import get_user_data, update_bet
from Logic import MAX_BET, MIN_BET

from ..additional_functoins import play_game
from ..Keyboards import game_keyboard
from ..print_functions import send_game

router = Router()


class BalanceState(StatesGroup):
    entering_bet = State()


@router.callback_query(lambda callback: callback.data == "button_bet")
async def handle_bet_button(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer(
        f"Введите ставку от {MIN_BET} до {MAX_BET}:"
    )
    await state.set_state(BalanceState.entering_bet)
    await callback_query.answer()


@router.message(BalanceState.entering_bet)
async def process_bet_input(message: Message):
    user_data = await get_user_data(message.chat.id)
    current_balance = user_data.balance
    main_message_id = user_data.main_message_id
    try:
        input_bet = float(message.text)
        if MIN_BET <= input_bet <= current_balance:
            await update_bet(message.chat.id, round(input_bet, 2))

            await message.reply(f"Ваша ставка установлена: {input_bet}💰")

            if main_message_id:
                await message.bot.delete_message(chat_id=message.chat.id, message_id=main_message_id)

            await send_game(message, game_keyboard)

        else:
            await message.reply(f"Ставка должна быть в пределах от {MIN_BET} "
                                f"до {current_balance}. Попробуйте снова.")
    except ValueError:
        await message.reply(f"Введите корректное число от {MIN_BET} до {current_balance}.")


@router.callback_query(lambda callback: callback.data == "button_spin")
async def handle_button_spin(callback_query: types.CallbackQuery, state: FSMContext):
    await play_game(callback_query, state)
    await callback_query.answer()


@router.callback_query(lambda callback: callback.data == "disable")
async def disable_button(callback_query: types.CallbackQuery):
    await callback_query.answer()
