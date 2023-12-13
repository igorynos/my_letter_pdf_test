from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import db
from keyboards.default.cont_user import cont_user

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
