from aiogram.types import Message, CallbackQuery
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from ..additional_functoins import send_game, play_game
from Logic import BALANCE

router = Router()
bet = 10

class BalanceState(StatesGroup):
    entering_bet = State()

@router.callback_query(lambda callback: callback.data == "button_bet")
async def handle_bet_button(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer(
        "Введите ставку от 10 до 10000:"
    )
    await state.set_state(BalanceState.entering_bet)
    await callback_query.answer()


@router.message(BalanceState.entering_bet)
async def process_bet_input(message: Message, state: FSMContext):
    try:
        input_bet = float(message.text)
        if 10 <= input_bet <= 10000:
            await state.update_data(bet=input_bet)

            await message.reply(f"Ваша ставка установлена: {input_bet}💰")
            data = await state.get_data()
            main_slot_id = data.get("main_slot")

            if main_slot_id:
                await message.bot.delete_message(chat_id=message.chat.id, message_id=main_slot_id)

            await send_game(message, state, BALANCE)

        else:
            await message.reply("Ставка должна быть в пределах от 0.1 до 1000. Попробуйте снова.")
    except ValueError:
        await message.reply("Введите корректное число от 0.1 до 1000.")


@router.callback_query(lambda callback: callback.data == "button_spin")
async def handle_button_spin(callback_query: types.CallbackQuery, state: FSMContext):
    await play_game(callback_query.message, state, BALANCE,
                    is_private_chat=callback_query.message.chat.type == "private")
    await callback_query.answer()

@router.callback_query(lambda callback: callback.data == "disable")
async def disable_button(callback_query: types.CallbackQuery):
    await callback_query.answer()