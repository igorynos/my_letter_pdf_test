from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


button1 = KeyboardButton(
    text="Создать письмо")
button2 = KeyboardButton(
    text="Мои реквизиты")
button3 = KeyboardButton(text="Получатели")
button4 = KeyboardButton(text="Шаблоны")
button5 = KeyboardButton(
    text="Словарь операндов")


menu_start_admin = ReplyKeyboardMarkup(resize_keyboard=True).row(
    button1).row(button2, button3).row(button4, button5)

menu_start_user = ReplyKeyboardMarkup(resize_keyboard=True).row(
    button1).row(button2, button3)
