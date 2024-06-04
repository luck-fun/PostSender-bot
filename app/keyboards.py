from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Add channel")], [KeyboardButton(text="Remove channel")],
    [KeyboardButton(text="My channel")],
    [KeyboardButton(text="Send post")]
],
    resize_keyboard=True,
    input_field_placeholder='Choose one')