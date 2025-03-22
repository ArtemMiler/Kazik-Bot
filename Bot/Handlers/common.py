from aiogram import Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from Database import get_user_data, add_user_data, update_message_id
from ..Keyboards.all_keyboards import game_keyboard, start_keyboard
from ..print_functions import send_game

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    main_slot_id = await check_user_in_db(message)
    if message.chat.type == "private":
        if main_slot_id:
            try:
                await message.bot.delete_message(chat_id=message.chat.id, message_id=main_slot_id)
            except Exception as e:
                print(f"Error deleting message: {e}")

        await message.answer(
            "Выберите режим игры:",
            reply_markup=start_keyboard
        )
    else:
        await send_game(message, game_keyboard)


async def check_user_in_db(message):
    user_data = await get_user_data(message.chat.id)
    if not user_data:
        await add_user_data(message.chat.id)
        user_data = await get_user_data(message.chat.id)

    if not user_data.main_message_id:
        await update_message_id(message.chat.id, message.message_id)

    return user_data.main_message_id


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
async def demo_button_handler(callback_query: CallbackQuery):
    await callback_query.message.delete()
    await send_game(callback_query.message, game_keyboard)
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
