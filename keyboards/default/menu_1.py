from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu_1 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Создать письмо"),

            KeyboardButton(text="Мои реквизиты"),
            KeyboardButton(text="Получатели")
        ],
        [
            KeyboardButton(text="Шаблоны"),
            KeyboardButton(text="Словарь операндов")
        ]
    ],
    resize_keyboard=True
)
