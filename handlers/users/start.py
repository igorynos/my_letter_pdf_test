from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import dp
from loader import db
from loader import bot

from states.letter import State_list

import io

from keyboards.inline.choise_template import choice
from keyboards.inline.choise_template import menu_template
from keyboards.inline.choise_template import delete_choice
from keyboards.inline.change_user_card import change_card
from keyboards.inline.change_user_card import user_card
from keyboards.inline.choise_cont_user import choise_cont_user, change_cont_card, nest_pars, cont_user, cont_user_2
from keyboards.inline.callback_data import template, del_template, change_my_card, cont_user_choise, change_cont_user_choise
from keyboards.inline.menu_start import menu_start


import random

import pymysql

import urllib.request

import docx
import io
import urllib.request
import re
from docx2pdf import convert
import aiohttp

dict_temp = {}
dict_column_name = {"name": 'ФИО изменено',
                    "status": 'Статус изменен',
                    "adress": 'Адрес изменен',
                    "phone": 'Телефон изменен',
                    "email": 'Email изменен',
                    "inn": 'ИНН изменен',
                    "pasport": 'Паспорт изменен',
                    "born": 'Дата рождения изменено',
                    "comment": 'Коментарий изменен'}


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    sql = f"SELECT * FROM users WHERE id = '{message.chat.id}';"
    result = db.execute(sql, fetchone=True)
    if result is None:
        await message.answer(f"Привет, {message.from_user.full_name}!")
        name = message.from_user.full_name

        try:
            db.add_user(id=message.from_user.id, name=name)
        except pymysql.IntegrityError as err:
            print(err)
        await message.answer("Напиши своё ФИО")
        await state.set_state("FIO")
    else:
        await message.answer(f"Выберите действие:", reply_markup=menu_start)


@dp.callback_query_handler(text='В начало')
async def in_start(call: types.CallbackQuery, state: FSMContext):
    await bot_start(message=call.message, state=state)


@dp.callback_query_handler(text='Словарь операндов')
async def dict_oper(call: types.CallbackQuery):
    text = ('{{name}} - Имя пользователя\n\
{{adress}} - Адресс пользователя\n\
{{phone}} - Телефон пользователя\n\
{{email}} - Email пользователя\n\
{{inn}} - ИНН пользователя\n\
{{pasport}} - Пасспорт пользователя\n\
{{born}} - Дата рождения пользователя\n\
{{comment}} - Комментарий пользователя\n\
{{cont_name}} - Имя получателя\n\
{{cont_adress}} - Адрес получателя\n\
{{cont_phone}} - Телефон получателя\n\
{{cont_email}} - Email получателя\n\
{{cont_inn}} - ИНН получателя\n\
{{cont_pasport}} - Паспорт получателя\n\
{{cont_born}} - Дата рождения получателя\n\
{{cont_comment}} - Комментарий получателя\n\
{{data}} - Дата')
    await call.message.answer(text=text, reply_markup=menu_start)


@dp.message_handler(state="FIO")
async def enter_name(message: types.Message, state: FSMContext):
    name = message.text
    db.update_user(name=name, id=message.from_user.id)
    await message.answer(
        "\n".join([
            f"{name} Занесён в базу"
        ])
    )
    await state.finish()
    await message.answer(f"Выберите действие:", reply_markup=menu_start)


@dp.message_handler(text='Создать письмо')
async def enter_test(message: types.Message):
    await choice(message)


@dp.callback_query_handler(text='Получатели')
async def enter_test(call: types.CallbackQuery):
    await choise_cont_user(call.message)


@dp.callback_query_handler(text='Добавить шаблон')
async def new_tamplate(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Название шаблона")
    await state.set_state("name_tamplate")


@dp.callback_query_handler(text='Шаблоны')
async def tamplates(call: types.CallbackQuery):
    await bot.send_message(chat_id=call.message.chat.id, text="Выберите действие", reply_markup=menu_template)


@dp.callback_query_handler(text='Удалить шаблон')
async def delete_tamplate(call: types.CallbackQuery):
    await delete_choice(call.message)


@dp.callback_query_handler(text='Мои реквизиты')
async def my_user_card(call: types.CallbackQuery):
    sql = f"SELECT * FROM users WHERE id='{call.message.chat.id}'"
    my_card = db.execute(sql, fetchall=True, commit=True)
    my_card = my_card[0]

    text = f"#myinfo (@{call.message.chat.username})\n\n\
{my_card[1]}\n\
Адрес: {my_card[3]}\n\
Тел: {my_card[4]}\n\
Email: {my_card[5]}\n\
ИНН: {my_card[6]}\n\
Паспорт: {my_card[7]}\n\
Дата рождения: {my_card[8]}\n\
Комментарий: {my_card[9]}"
    await bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=user_card)


@dp.callback_query_handler(cont_user_choise.filter())
async def cont_user_card(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    quantity = callback_data.get('id')
    sql = f"SELECT * FROM cont_users WHERE id='{quantity}'"
    my_card = db.execute(sql, fetchall=True, commit=True)
    my_card = my_card[0]
    dict_temp[f'{call.message.chat.id}'] = quantity

    text = f"{my_card[0]}\n\
Адрес: {my_card[2]}\n\
Тел: {my_card[3]}\n\
Email: {my_card[4]}\n\
ИНН: {my_card[5]}\n\
Паспорт: {my_card[6]}\n\
Дата рождения: {my_card[7]}\n\
Комментарий: {my_card[8]}"
    await bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=cont_user_2)


@dp.callback_query_handler(text='Изменить')
async def my_user_card_2(call: types.CallbackQuery):
    await change_card(call.message)


@dp.callback_query_handler(text='Изменить данные')
async def cont_user_card_2(call: types.CallbackQuery):
    await change_cont_card(call.message, dict_temp[f'{call.message.chat.id}'])


@dp.message_handler(state="name_tamplate")
async def name_acc(message: types.Message, state: FSMContext):
    name = message.text

    await state.update_data(
        {
            'name': name
        }
    )
    await message.answer("Вставьте ссылку на шаблон в Google docs")
    await message.answer("В формате 'https://docs.google.com/document/пример/пример/edit'")
    await state.set_state("link_template")


@dp.message_handler(state="link_template")
async def link_template(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name = data.get("name")
    link_template = message.text
    link_template = link_template.replace("/edit", "/export?format=docx")

    db.add_template(name=name, link=link_template,
                    template_id=random.randint(1000000, 9999999))

    await state.finish()

    await message.answer(text=f'Новый шаблон {name} создан')


@dp.callback_query_handler(del_template.filter())
async def letter(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    quantity = callback_data.get('id')
    sql_name = f"SELECT name FROM template WHERE id = '{quantity}'"
    name = db.execute(sql_name, fetchone=True)
    sql = f"DELETE FROM template WHERE id = '{quantity}'"
    db.execute(sql, fetchall=True, commit=True)

    await call.message.answer(text=f'Шаблон {name[0]} удалён')
    await tamplates(call=call)


@dp.callback_query_handler(change_my_card.filter())
async def change_card_2(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    quantity = callback_data.get('name')

    await state.update_data(
        {
            f'answer': quantity
        }
    )

    await call.message.answer("Напишите новое значение")
    await state.set_state("change_card_3")


@dp.callback_query_handler(change_cont_user_choise.filter())
async def change_cont_card_2(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    quantity = callback_data.get('parametr')
    id_cont = callback_data.get('name')
    print(quantity)
    print(id_cont)

    await state.update_data(
        {
            f'answer': quantity,
            f'id': id_cont
        }
    )

    await call.message.answer(f"Напишите новое значение")
    await state.set_state("change_cont_card_3")


@dp.message_handler(state="change_card_3")
async def change_card_3(message: types.Message, state: FSMContext):
    data = await state.get_data()
    answer1 = data.get("answer")
    answer2 = message.text

    sql = f"UPDATE users SET {answer1} = '{answer2}' WHERE id = {message.chat.id}"
    db.execute(sql, fetchone=True, commit=True)
    await state.finish()
    await message.answer(f"{dict_column_name[f'{answer1}']}")

    call = CallbackQuery()
    call['message'] = message
    await my_user_card(call)


@dp.message_handler(state="change_cont_card_3")
async def change_cont_card_3(message: types.Message, state: FSMContext):
    data = await state.get_data()
    answer1 = data.get("answer")
    id_cont = data.get("id")
    answer2 = message.text
    dict_column_name = {"name": 'ФИО изменено',
                        "status": 'Статус изменен',
                        "adress": 'Адрес изменен',
                        "phone": 'Телефон изменен',
                        "email": 'Email изменен',
                        "inn": 'ИНН изменен',
                        "pasport": 'Паспорт изменен',
                        "born": 'Дата рождения изменено',
                        "comment": 'Коментарий изменен'}

    sql = f"UPDATE cont_users SET {answer1} = '{answer2}' WHERE user = %s AND id = %s"
    db.execute(sql, parameters=(message.chat.id, id_cont),
               fetchall=True, commit=True)
    await state.finish()
    await message.answer(f"{dict_column_name[f'{answer1}']}", reply_markup=cont_user_2)
