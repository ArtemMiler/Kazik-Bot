import asyncio

from aiogram import types

from Bot.Keyboards import disable_bonus_keyboard, disable_game_keyboard
from Database import get_user_data, update_message_id
from Logic.Settings import *
from Logic.Spin import SlotCheck


async def smooth_transform(matrix2, message, chat_id):
    async def format_with_state(matrix):
        return await format_message_matrix(matrix, chat_id)
    await smooth_transform_common(matrix2, message, edit_message, format_with_state)


async def smooth_bonus_transform(matrix2, message, chat_id):
    async def format_with_state(matrix):
        return await format_message_matrix(matrix, chat_id)
    await smooth_transform_common(matrix2, message, edit_bonus_message, format_with_state)


async def smooth_transform_common(matrix2, obj, edit_func, format_func):
    slot_check = SlotCheck()
    matrix1 = [row[:] for row in slot_check.win_slot]

    if isinstance(obj, types.CallbackQuery):
        chat_type = obj.message.chat.type
        message = obj.message
    else:
        chat_type = obj.chat.type
        message = obj

    for col in range(COLS):
        for row in range(ROWS):
            matrix1[row][col] = matrix2[row][col]
            if chat_type == 'private':
                text = await format_func(matrix1)
                await edit_func(text, message)
                await asyncio.sleep(0.2)

        if chat_type != 'private':
            text = await format_func(matrix1)
            await edit_func(text, message)
            await asyncio.sleep(1.0)
    await asyncio.sleep(1.5)


async def format_message_check(check, chat_id, win=0):
    return await format_message_base(check, chat_id, win)


async def format_message_matrix(matrix, chat_id):
    return await format_message_base(matrix, chat_id)


async def format_message_base(content, chat_id, win=0):
    user_data = await get_user_data(chat_id)
    bet = user_data.bet
    balance = user_data.balance
    free_spins = user_data.free_spin

    base_text = (
        f"<b>JOKER CASINO</b>\n"
        f"{print_list(content.win_slot if isinstance(content, SlotCheck) else content)}\n"
        f"<b>Баланс: </b>{float(balance)}\n"
        f"<b>Ставка: </b>{float(bet)}"
    )

    bonus_text = f"\n<b>FREE SPINS: </b>{free_spins}" if free_spins >= 0 else ""

    win_text = ""
    ways_text = ""
    if isinstance(content, SlotCheck) and win > 0:
        win_text = (f"\n<b>Выигрыш: </b>{float(win)}\n"
                    f"x{round(float(win) / float(bet), 2)}\n"
                    )
        if content.ways > 0:
            ways_text = f"<b>Количество путей: </b>{content.ways}"

    return base_text + bonus_text + win_text + ways_text


async def send_game(message, kb):
    user_data = await get_user_data(message.chat.id)
    main_slot_id = user_data.main_message_id

    if main_slot_id:
        try:
            await message.bot.delete_message(message.chat.id, main_slot_id)
        except Exception as e:
            print(f"Ошибка при удалении предыдущего сообщения: {e}")

    my_check = SlotCheck()

    text = await format_message_check(my_check, message.chat.id)
    sent_message = await print_message(text, kb, message)
    await update_message_id(message.chat.id, sent_message.message_id)


def print_list(matrix):
    return '\n'.join('|' + '|'.join(row) + '|' for row in matrix)


async def print_message(text, kb, message):
    return await message.answer(
        text,
        parse_mode="HTML",
        reply_markup=kb
    )


async def edit(text, kb, message):
    return await message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=kb
    )


async def edit_message(text, message):
    return await message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=disable_game_keyboard
    )


async def edit_bonus_message(text, message):
    return await message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=disable_bonus_keyboard
    )
