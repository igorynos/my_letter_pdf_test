from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


cont_user = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить получателя"),
            KeyboardButton(text="Удалить получателя"),
            KeyboardButton(text="В начало")
        ],
    ],
    resize_keyboard=True
)

cont_user_2 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Изменить данные"),
            KeyboardButton(text="В начало")
        ],
    ],
    resize_keyboard=True
)

nest_pars = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Пропустить"),
        ],
    ],
    resize_keyboard=True
)
