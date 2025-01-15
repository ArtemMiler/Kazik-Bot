import asyncio

from .Keyboards import game_keyboard
from Logic import SlotCheck, SlotSpin, WinCount
from Logic.Settings import ROWS, COLS
from .Keyboards.gamemode import disable_game_keyboard


async def smooth_transform(matrix1, matrix2, message, balance, bet, is_private_chat):
    for col in range(COLS):
        for row in range(ROWS):
            matrix1[row][col] = matrix2[row][col]
            if is_private_chat:
                await print_message(matrix1, bet, balance, 0, 0, disable_game_keyboard, message, True)
                await asyncio.sleep(0.2)

        if not is_private_chat:
            await print_message(matrix1, bet, balance, 0, 0, disable_game_keyboard, message, True)
            await asyncio.sleep(1.0)
    await asyncio.sleep(1.5)

async def send_game(message, state, balance):
    data = await state.get_data()
    bet = data.get("bet", 10)
    my_check = SlotCheck()

    sent_message = await print_message(my_check.win_slot, bet, balance, 0, 0, game_keyboard, message, False)
    await state.update_data(main_slot=sent_message.message_id)

def print_list(matrix):
    return '\n'.join('|' + '|'.join(row) + '|' for row in matrix)

async def play_game(message, state, balance, is_private_chat):
    data = await state.get_data()
    bet = data.get("bet", 10)
    check = SlotCheck()
    before_slot = check.win_slot

    spin = SlotSpin()
    current_slot = spin.slot

    await smooth_transform(before_slot, current_slot, message, balance, bet, is_private_chat)

    check.check_win(spin.slot)
    win = WinCount(bet)
    await print_message(check.win_slot, bet, balance, win.count_win(check), check.ways, game_keyboard, message, True)

async def print_message(matrix, bet_, balance_, win_, ways, kb, message, is_edit):
    if win_ == 0:
        text = (
            f"<b>JOKER CASINO</b>\n"
            f"{print_list(matrix)}\n"
            f"<b>Баланс: </b>{float(balance_)}\n"
            f"<b>Ставка: </b>{float(bet_)}"
        )
    else:
        text = (
            f"<b>JOKER CASINO</b>\n"
            f"{print_list(matrix)}\n"
            f"<b>Баланс: </b>{float(balance_)}\n"
            f"<b>Ставка: </b>{float(bet_)}\n"
            f"<b>Выигрыш: </b>{float(win_)}\n"
            f"x{round(float(win_) / float(bet_), 2)}\n"
            f"<b>Количество путей: </b>{ways}"
        )
    if is_edit:
        return await message.edit_text(
            text,
            parse_mode="HTML",
            reply_markup=kb
        )
    else:
        return await message.answer(
            text,
            parse_mode="HTML",
            reply_markup=kb
        )