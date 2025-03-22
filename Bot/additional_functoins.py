from Database import get_user_data, add_balance
from Logic import *
from Logic.Settings import *

from .Keyboards import bonus_keyboard, game_keyboard
from .print_functions import edit, format_message_check, smooth_transform


async def play_game(callback_query, state):
    chat_id = callback_query.message.chat.id
    user_data = await get_user_data(chat_id)

    if user_data.bet <= user_data.balance:
        await add_balance(chat_id, -user_data.bet)

        spin = SlotSpin()
        current_slot = spin.slot

        await smooth_transform(current_slot, callback_query.message, chat_id)

        check = SlotCheck(spin.slot)
        check.check_win()
        win = WinCount(user_data.bet)
        win_sum = win.count_win(check)
        await add_balance(chat_id, win_sum)
        text = await format_message_check(check, chat_id, win_sum)
        await edit(text, game_keyboard, callback_query.message)

        if check.count_bonus():
            bonus_type = check.count_bonus() - MIN_BONUS_QUANTITY
            await find_bonus(callback_query, state, bonus_type)
    elif user_data.balance < MIN_BET:
        await callback_query.answer(f"Не достаточно средств на Балансе! "
                                    f"Ожидайте пополнение счета завтра",
                                    show_alert=True)
    else:
        await callback_query.answer("Уменьшите ставку", show_alert=True)


async def find_bonus(callback_query, state, bonus_type):

    await callback_query.answer(
        "Поздравляем с выигрышем бонусной игры 🎰",
        show_alert=True
    )

    await state.update_data(
        bonus_type=bonus_type,
        free_spins=BONUS_CONDITIONALS.get(bonus_type)
    )
    check = SlotCheck()
    text = await format_message_check(check, callback_query.message.chat.id)
    await edit(text, bonus_keyboard, callback_query.message)


async def play_bonus_game(bonus, state):
    data = await state.get_data()
    bonus_type = data.get("bonus_type", 0)

    bonus_classes = {
        0: Bonus,
        1: SuperBonus,
        2: MegaBonus
    }

    bonus = bonus_classes.get(bonus_type, Bonus)(bonus.callback_query, state)
    await bonus.initialize()
    await bonus.play_bonus()
