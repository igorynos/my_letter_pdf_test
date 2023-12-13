from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import db

from keyboards.inline.callback_data import template, del_template, change_my_card

from aiogram import types


async def change_card(message: types.Message):
    sql = f"SHOW COLUMNS FROM users"
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
    for x in name_column[1:]:
        change_card.add(InlineKeyboardButton(
            text=dict_column_name[f'{x}'], callback_data=change_my_card.new(name=x)))
    await message.answer("Выберите параметр", reply_markup=change_card)
