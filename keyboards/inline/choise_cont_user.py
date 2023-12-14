from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import db

from keyboards.inline.callback_data import cont_user_choise, change_cont_user_choise, dell_cont_user_choise, letter_cont_user_choise

from aiogram import types


async def choise_cont_user(message: types.Message):
    lst_template = [item[0] for item in db.execute(
        f"SELECT name FROM cont_users WHERE user = {message.chat.id}", fetchall=True)]
    choice = InlineKeyboardMarkup(row_width=2)
    for x in lst_template:
        choice.add(InlineKeyboardButton(
            text=x, callback_data=cont_user_choise.new(name=x)))
    await message.answer("Выберите получателя", reply_markup=choice)
    await message.answer("Выберите действие", reply_markup=cont_user)


async def letter_choise_cont_user(message: types.Message):
    lst_template = [item[0] for item in db.execute(
        f"SELECT name FROM cont_users WHERE user = {message.chat.id}", fetchall=True)]
    choice = InlineKeyboardMarkup(row_width=2)
    for x in lst_template:
        choice.add(InlineKeyboardButton(
            text=x, callback_data=letter_cont_user_choise.new(name=x)))
    await message.answer("Выберите получателя", reply_markup=choice)


async def dell_choise_cont_user(message: types.Message):
    lst_template = [item[0] for item in db.execute(
        f"SELECT name FROM cont_users WHERE user = {message.chat.id}", fetchall=True)]
    choice = InlineKeyboardMarkup(row_width=2)
    for x in lst_template:
        choice.add(InlineKeyboardButton(
            text=x, callback_data=dell_cont_user_choise.new(name=x)))
    await message.answer("Выберите получателя", reply_markup=choice)
#


async def change_cont_card(message: types.Message):
    sql = f"SHOW COLUMNS FROM cont_users"
    name_column = db.execute(sql, fetchall=True, commit=True)
    name_column = [item[0] for item in name_column]
    print(name_column)
    dict_column_name = {"name": 'ФИО',
                        "status": 'Статус',
                        "adress": 'Адрес',
                        "phone": 'Телефон',
                        "email": 'Email',
                        "inn": 'ИНН',
                        "pasport": 'Паспорт',
                        "born": 'Дата рождения',
                        "comment": 'Коментарий'}

    change_card = InlineKeyboardMarkup(row_width=3)
    for x in name_column[:-1]:
        change_card.add(InlineKeyboardButton(
            text=dict_column_name[f'{x}'], callback_data=change_cont_user_choise.new(name=x)))
    await message.answer("Выберите параметр", reply_markup=change_card)


user_button1 = InlineKeyboardButton(
    text="Добавить получателя", callback_data="Добавить получателя")
user_button2 = InlineKeyboardButton(
    text="Удалить получателя", callback_data="Удалить получателя")
user_button3 = InlineKeyboardButton(text="В начало", callback_data="В начало")

cont_user = InlineKeyboardMarkup().row(
    user_button1, user_button2).row(user_button3)


user2_button1 = InlineKeyboardButton(
    text="Изменить данные", callback_data="Изменить данные")
user2_button2 = InlineKeyboardButton(text="В начало", callback_data="В начало")

cont_user_2 = InlineKeyboardMarkup().row(user2_button1).row(user2_button2)


nest_pars_button = InlineKeyboardButton(
    text="Пропустить", callback_data="Пропустить")

nest_pars = InlineKeyboardMarkup().add(nest_pars_button)
