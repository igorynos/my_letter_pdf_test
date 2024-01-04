from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import db

from keyboards.inline.callback_data import template, del_template

from aiogram import types


async def choice(message: types.Message):
    lst_template = [item[0] for item in db.execute(
        "SELECT name FROM template", fetchall=True)]
    lst_id = [item[0] for item in db.execute(
        "SELECT id FROM template", fetchall=True)]
    choice = InlineKeyboardMarkup(row_width=2)
    for i, x in enumerate(lst_template):
        choice.add(InlineKeyboardButton(
            text=x, callback_data=template.new(id=lst_id[i])))
    choice.add(InlineKeyboardButton(text="Отмена", callback_data="В начало"))
    await message.answer("Выберите шаблон:", reply_markup=choice)


async def delete_choice(message: types.Message):
    lst_template = [item[0] for item in db.execute(
        "SELECT name FROM template", fetchall=True)]
    lst_id = [item[0] for item in db.execute(
        "SELECT id FROM template", fetchall=True)]
    del_choice = InlineKeyboardMarkup(row_width=2)
    for i, x in enumerate(lst_template):
        del_choice.add(InlineKeyboardButton(
            text=x, callback_data=del_template.new(id=lst_id[i])))
    del_choice.add(InlineKeyboardButton(
        text="Отмена", callback_data="В начало"))
    await message.answer("Выберите шаблон", reply_markup=del_choice)


button1 = InlineKeyboardButton(
    text="Добавить шаблон", callback_data="Добавить шаблон")
button2 = InlineKeyboardButton(
    text="Удалить шаблон", callback_data="Удалить шаблон")
button3 = InlineKeyboardButton(text="В начало", callback_data="В начало")

menu_template = InlineKeyboardMarkup().add(button1, button2)
