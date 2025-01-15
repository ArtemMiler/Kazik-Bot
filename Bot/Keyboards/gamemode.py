from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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