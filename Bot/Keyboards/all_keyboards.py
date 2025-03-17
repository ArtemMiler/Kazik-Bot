from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Logic.Settings import BONUS_PRISE, MEGA_BONUS_PRISE, SUPER_BONUS_PRISE

start_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Реальный счет💸", callback_data="real_button"),
        InlineKeyboardButton(text="Демо-счет🥇", callback_data="demo_button")
    ]
])

game_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Крутить🔄", callback_data="button_spin")],
    [
        InlineKeyboardButton(text="Ставка💰", callback_data="button_bet"),
        InlineKeyboardButton(text="Купить бонус💎", callback_data="button_buy")
    ]
])

disable_game_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Крутить🔄", callback_data="disable")],
    [
        InlineKeyboardButton(text="Ставка💰", callback_data="disable"),
        InlineKeyboardButton(text="Купить бонус💎", callback_data="disable")
    ]
])

bonus_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🔄 Крутить 🔄", callback_data="bonus_spin"),
        InlineKeyboardButton(text="❌ Отмена ❌", callback_data="cancel")
    ]
])

disable_bonus_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🔄 Крутить 🔄", callback_data="disable"),
        InlineKeyboardButton(text="❌ Отмена ❌", callback_data="disable")
    ]
])

next_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="⏩ Далее ⏩", callback_data="next"),
        InlineKeyboardButton(text="Купить ещё💎", callback_data="button_buy")
    ]
])


async def select_bonus(bet: int):
    select_bonus_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"🥉Обычный {bet * BONUS_PRISE}", callback_data="bonus")],
        [InlineKeyboardButton(text=f"🥈Супер {bet * SUPER_BONUS_PRISE}", callback_data="super")],
        [InlineKeyboardButton(text=f"🥇Мега {bet * MEGA_BONUS_PRISE}", callback_data="mega")],
        [InlineKeyboardButton(text="⏪Назад", callback_data="back")]
    ])
    return select_bonus_keyboard
