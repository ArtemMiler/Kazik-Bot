from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from ..Keyboards.all_keyboards import game_keyboard, start_keyboard
from ..print_functions import send_game

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    if message.chat.type == "private":
        data = await state.get_data()
        main_slot_id = data.get("main_slot")
        if main_slot_id:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=main_slot_id)

        await message.answer(
            "Выберите режим игры:",
            reply_markup=start_keyboard
        )
    else:
        await send_game(message, state, game_keyboard)


@router.callback_query(lambda callback: callback.data == "real_button")
async def real_button_handler(callback_query: CallbackQuery):
    if callback_query.message.chat.type == "private":
        await callback_query.answer(
            "Режим игры на реальные средства в разработке",
            show_alert=True
        )
    else:
        await callback_query.answer(
            "Режим игры на реальные средства не доступен в группах",
            show_alert=True
        )


@router.callback_query(lambda callback: callback.data == "demo_button")
async def demo_button_handler(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await send_game(callback_query.message, state, game_keyboard)
    await callback_query.answer()


@router.message(Command("help"))
async def cmd_help(message):
    await message.answer(
        "🃏<b>JOKER CASINO</b>🃏 поддерживает режим игры только с игровой валютой\n\n"
        "Для выбора режима нажмите <b>/start</b>\n"
        "(<i>В группах доступен только демо-счет</i>)\n\n"
        "После этого для игры используйте кнопки для игры\n"
        "Игра представляет собой поле 3 x 5, которое случайным образом заполняется 11 символами.\n"
        "Вот они в порядке увеличения стоимости:\n"
        "[♠️, ♣️, ♥️, ♦️, 🍀, 🧿, 👑, 🔮, ⚜️, 🎰, 💎]\n\n"
        "<b>🎰 - Wild</b> символ, который может заменить собой любой из доступных. "
        "В соответствии с этой механикой он будет учитываться по собственной цене "
        "<b>только</b> в линии из 5 элементов.\n\n"
        "<b>💎 - Bonus</b> символ сам по себе в комбинациях не участвует "
        "и не имеет никакой стоимости, "
        "но считается по всему полю и активирует <b>Bonus Game</b>:\n"
        "  • <b>х3💎</b> - фиксирует максимальный выигрыш\n"
        "  • <b>х4💎</b> - Wild столбцы\n"
        "  • <b>х5💎</b> - \"липкий\" Wild\n\n"
        "В случае нахождения багов, ошибок или предложений по улучшению пишите <i>@ama_8800</i>.",
        parse_mode="HTML"
    )
