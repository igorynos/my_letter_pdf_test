from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from loader import db
from loader import dp

from keyboards.inline.callback_data import cont_user_choise, change_cont_user_choise, dell_cont_user_choise, letter_cont_user_choise, change_and_name

from aiogram.dispatcher.storage import FSMContext

import random

from aiogram import types

from dadata import Dadata


async def choise_cont_user(message: types.Message):
    lst_template = [item[0] for item in db.execute(
        f"SELECT org FROM cont_users WHERE user = {message.chat.id}", fetchall=True)]
    lst_id = [item[0] for item in db.execute(
        f"SELECT id FROM cont_users WHERE user = {message.chat.id}", fetchall=True)]
    choice = InlineKeyboardMarkup(row_width=2)
    for i, x in enumerate(lst_template):
        choice.add(InlineKeyboardButton(
            text=x, callback_data=cont_user_choise.new(id=lst_id[i])))
    await message.answer("Выберите получателя:", reply_markup=choice)
    await message.answer("Выберите действие:", reply_markup=cont_user)


async def letter_choise_cont_user(message: types.Message, state: FSMContext):
    lst_template = [item[0] for item in db.execute(
        f"SELECT org FROM cont_users WHERE user = {message.chat.id}", fetchall=True)]
    lst_id = [item[0] for item in db.execute(
        f"SELECT id FROM cont_users WHERE user = {message.chat.id}", fetchall=True)]
    print(lst_template)
    if len(lst_template) == 0:
        await message.answer("Напишите ИНН получателя", reply_markup=nest_pars)
        await state.set_state("add_cont_user_name")
    else:
        choice = InlineKeyboardMarkup(row_width=2)
        for i, x in enumerate(lst_template):
            choice.add(InlineKeyboardButton(
                text=x, callback_data=letter_cont_user_choise.new(id=lst_id[i])))
        choice.add(InlineKeyboardButton(
            text="Добавить получателя", callback_data="Добавить получателя"))
        await message.answer("Выберите получателя", reply_markup=choice)


async def dell_choise_cont_user(message: types.Message):
    lst_template = [item[0] for item in db.execute(
        f"SELECT org FROM cont_users WHERE user = {message.chat.id}", fetchall=True)]
    lst_id = [item[0] for item in db.execute(
        f"SELECT id FROM cont_users WHERE user = {message.chat.id}", fetchall=True)]
    choice = InlineKeyboardMarkup(row_width=2)
    for i, x in enumerate(lst_template):
        choice.add(InlineKeyboardButton(
            text=x, callback_data=dell_cont_user_choise.new(id=lst_id[i])))
    await message.answer("Выберите получателя", reply_markup=choice)
#


async def change_cont_card(message: types.Message, name=None):
    sql = f"SHOW COLUMNS FROM cont_users"
    name_column = db.execute(sql, fetchall=True, commit=True)
    name_column = [item[0] for item in name_column]
    dict_column_name = {"org": f'Наименование организации получателя',
                        "ogrn": f'ОГРН организации получателя',
                        "adress": f'Почтовый адрес организации получателя',
                        "phone": f'Телефон представителя организации получателя',
                        "email": f'Email организации получателя',
                        "inn": f'ИНН организации получателя',
                        "pasport": f'Паспорт получателя',
                        "born": f'Дату рождения получателя',
                        "comment": f'Комментарий (статус) организации получателя',
                        "fio": f'ФИО руководителя организации получателя',
                        "headstatus": f'Должность руководителя организации получателя',
                        "fiocont": f'ФИО представителя организации получателя',
                        "link": f'Ссылку на организацию получателя'}

    change_card = InlineKeyboardMarkup(row_width=3)
    for x in name_column[:-2]:
        change_card.add(InlineKeyboardButton(
            text=dict_column_name[f'{x}'], callback_data=change_cont_user_choise.new(name=name, parametr=x)))
    await message.answer("Выберите параметр", reply_markup=change_card)


user_button1 = InlineKeyboardButton(
    text="Добавить получателя", callback_data="Добавить получателя")
user_button2 = InlineKeyboardButton(
    text="Удалить получателя", callback_data="Удалить получателя")
user_button3 = InlineKeyboardButton(text="В начало", callback_data="В начало")

cont_user = InlineKeyboardMarkup().row(
    user_button1, user_button2)


user2_button1 = InlineKeyboardButton(
    text="Изменить данные", callback_data="Изменить данные")
user2_button2 = InlineKeyboardButton(text="В начало", callback_data="В начало")

cont_user_2 = InlineKeyboardMarkup().row(user2_button1)


ask_dell_1 = InlineKeyboardButton(
    text="Да", callback_data="dell_yes")
ask_dell_2 = InlineKeyboardButton(text="Нет", callback_data="dell_no")

accept_dell = InlineKeyboardMarkup().row(ask_dell_1, ask_dell_2)


nest_pars_button = KeyboardButton(
    text="Пропустить")

nest_pars = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True).add(nest_pars_button)


@dp.message_handler(state='add_cont_user_name')
async def add_cont_user_name(message: types.Message, state: FSMContext):
    name = message.text
    token = "20473d0a0f63fdc5c6921b0d9b54ae2ca0745429"
    dadata = Dadata(token)
    data = dadata.find_by_id("party", name)

    if data != []:
        company_info = data[0]
        id_cont = random.randint(1000000, 9999999)
        db.add_cont_user(org=company_info['value'],
                         ogrn=company_info['data']['ogrn'],
                         adress=company_info['data']['address']['unrestricted_value'],
                         fio=company_info['data']['management']['name'],
                         headstatus=company_info['data']['management']['post'],
                         inn=name,
                         id=id_cont,
                         user=message.chat.id)
        await message.answer(f"Получатель {company_info['value']} создан")
        choice = InlineKeyboardMarkup(row_width=2)
        choice.add(InlineKeyboardButton(
            text=name, callback_data=letter_cont_user_choise.new(id=id_cont)))
        await message.answer("Выберите получателя", reply_markup=choice)
        await state.finish()
    else:
        await state.update_data(
            {
                'inn': name
            }
        )
        await message.answer("Напишите наименование организации получателя")
        await state.set_state("add_cont_user_name_2")


@dp.message_handler(state='add_cont_user_name_2')
async def add_cont_user_name2(message: types.Message, state: FSMContext):
    name = message.text
    id_cont = random.randint(1000000, 9999999)
    db.add_cont_user(org=name, user=message.chat.id, id=id_cont)
    choice = InlineKeyboardMarkup(row_width=2)
    choice.add(InlineKeyboardButton(
        text=name, callback_data=letter_cont_user_choise.new(id=id_cont)))
    await message.answer("Выберите получателя", reply_markup=choice)
    await state.finish()
