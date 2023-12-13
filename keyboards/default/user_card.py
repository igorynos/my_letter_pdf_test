from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


user_card = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Изменить"),
            KeyboardButton(text="В начало")
        ],
    ],
    resize_keyboard=True
)
