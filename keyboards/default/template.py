from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu_template = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить шаблон"),
            KeyboardButton(text="Удалить шаблон"),
            KeyboardButton(text="В начало")
        ],
    ],
    resize_keyboard=True
)
