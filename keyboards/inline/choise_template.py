from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import db

from keyboards.inline.callback_data import template, del_template

from aiogram import types


async def choice(message: types.Message):
    lst_template = [item[0] for item in db.execute(
        "SELECT name FROM template", fetchall=True)]
    choice = InlineKeyboardMarkup(row_width=2)
    for x in lst_template:
        choice.add(InlineKeyboardButton(
            text=x, callback_data=template.new(name=x)))
    await message.answer("Выберите шаблон", reply_markup=choice)


async def delete_choice(message: types.Message):
    lst_template = [item[0] for item in db.execute(
        "SELECT name FROM template", fetchall=True)]
    del_choice = InlineKeyboardMarkup(row_width=2)
    for x in lst_template:
        del_choice.add(InlineKeyboardButton(
            text=x, callback_data=del_template.new(name=x)))
    await message.answer("Выберите шаблон", reply_markup=del_choice)
