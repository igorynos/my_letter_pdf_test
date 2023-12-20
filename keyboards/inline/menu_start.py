from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


button1 = InlineKeyboardButton(
    text="Создать письмо", callback_data="Создать письмо")
button2 = InlineKeyboardButton(
    text="Мои реквизиты", callback_data="Мои реквизиты")
button3 = InlineKeyboardButton(text="Получатели", callback_data="Получатели")
button4 = InlineKeyboardButton(text="Шаблоны", callback_data="Шаблоны")
button5 = InlineKeyboardButton(
    text="Словарь операндов", callback_data="Словарь операндов")


menu_start_admin = InlineKeyboardMarkup().row(
    button1).row(button2, button3).row(button4, button5)

menu_start_user = InlineKeyboardMarkup().row(
    button1).row(button2, button3)
