import asyncio

from aiogram import types

from Bot.Keyboards import disable_bonus_keyboard, disable_game_keyboard
from Logic.Settings import *
from Logic.Spin import SlotCheck


async def smooth_transform(matrix2, message, state):
    async def format_with_state(matrix):
        return await format_message_matrix(matrix, state)
    await smooth_transform_common(matrix2, message, edit_message, format_with_state)


async def smooth_bonus_transform(matrix2, message, state):
    async def format_with_state(matrix):
        return await format_message_matrix(matrix, state)
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


async def format_message_check(check, state, win=0):
    return await format_message_base(check, state, win)


async def format_message_matrix(matrix, state):
    return await format_message_base(matrix, state)


async def format_message_base(content, state, win=0):
    data = await state.get_data()
    fs = data.get("free_spins", 0)
    bet = data.get("bet", BET)

    base_text = (
        f"<b>JOKER CASINO</b>\n"
        f"{print_list(content.win_slot if isinstance(content, SlotCheck) else content)}\n"
        f"<b>Баланс: </b>{float(BALANCE)}\n"
        f"<b>Ставка: </b>{float(bet)}"
    )

    bonus_text = f"\n<b>FREE SPINS: </b>{fs}" if fs >= 0 else ""

    win_text = ""
    if isinstance(content, SlotCheck) and win > 0:
        win_text = (f"\n<b>Выигрыш: </b>{float(win)}\n"
                    f"x{round(float(win) / float(bet), 2)}\n"
                    f"<b>Количество путей: </b>{content.ways}"
                    )

    return base_text + bonus_text + win_text


async def send_game(message, state, kb):
    data = await state.get_data()
    main_slot_id = data.get("main_slot")

    if main_slot_id:
        try:
            await message.bot.delete_message(message.chat.id, main_slot_id)
        except Exception as e:
            print(f"Ошибка при удалении предыдущего сообщения: {e}")

    my_check = SlotCheck()

    text = await format_message_check(my_check, state)
    sent_message = await print_message(text, kb, message)
    await state.update_data(main_slot=sent_message.message_id)


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
