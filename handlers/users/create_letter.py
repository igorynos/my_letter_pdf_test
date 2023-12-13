from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default import menu_1
from keyboards.default.user_card import user_card
from keyboards.default.template import menu_template
from keyboards.default.cont_user import cont_user_2


from loader import dp
from loader import db
from loader import bot
from loader import logger

from states.letter import State_list

import io

from keyboards.inline.choise_template import choice
from keyboards.inline.choise_template import delete_choice
from keyboards.inline.change_user_card import change_card
from keyboards.inline.choise_cont_user import choise_cont_user, change_cont_card, letter_choise_cont_user
from keyboards.inline.callback_data import template, del_template, change_my_card, cont_user_choise, change_cont_user_choise, letter_cont_user_choise

import pymysql

import urllib.request

import docx
import io
import urllib.request
import re
from docx2pdf import convert
import aiohttp

import subprocess


class Dict_user:
    dict_user_indx = {}
    dict_user_full_text = {}
    dict_user_answer = {}
    dict_user_call = {}


@dp.message_handler(text='Создать письмо')
async def enter_test(message: types.Message):
    await choice(message)


@dp.callback_query_handler(template.filter())
async def letter(call: CallbackQuery, callback_data: dict, state: FSMContext):
    logger.info(f"нажата кнопка {call}")
    await call.answer(cache_time=60)
    quantity = callback_data.get('name')

    sql = f"SELECT link FROM template WHERE name = '{quantity}'"
    link_template = db.execute(sql, fetchone=True)
    link_template = link_template[0]

    response = urllib.request.urlopen(link_template)
    async with aiohttp.ClientSession() as session:
        async with session.get(link_template) as response:
            if response.status == 200:
                content = await response.read()

                with io.BytesIO(content) as f:
                    doc = docx.Document(f)

                    full_text = []
                    for paragraph in doc.paragraphs:
                        if '{{' in paragraph.text:
                            text = paragraph.text
                            pattern = r'\{\{(.+?)\}\}'
                            matches = re.findall(pattern, text)
                            full_text.extend(matches)

    logger.info(f"запрос прошёл {full_text}")
    await letter_choise_cont_user(message=call.message)
    Dict_user.dict_user_full_text[f'{call.message.chat.id}'] = full_text
    Dict_user.dict_user_call[f'{call.message.chat.id}'] = link_template


@dp.callback_query_handler(letter_cont_user_choise.filter())
async def letter_2(call: CallbackQuery, callback_data: dict, state: FSMContext):
    logger.info(f"нажата кнопка 2 {call}")
    await call.answer(cache_time=60)
    quantity = callback_data.get('name')
    sql = f"SELECT * FROM cont_users WHERE name='{quantity}'"
    cont_card = db.execute(sql, fetchall=True, commit=True)
    cont_card = cont_card[0]
    sql = f"SELECT * FROM users WHERE id='{call.message.chat.id}'"
    my_card = db.execute(sql, fetchall=True, commit=True)
    my_card = my_card[0]

    await call.message.answer(text="Письмо создаётся...")

    dict_column_name = {"name": f'Имя пользователя',
                        "status": f'Статус пользователя',
                        "adress": f'Адресс пользователя',
                        "phone": f'Телефон пользователя',
                        "email": f'Email пользователя',
                        "inn": f'ИНН пользователя',
                        "pasport": f'Пасспорт пользователя',
                        "born": f'Дата рождения пользователя',
                        "comment": f'Комментарий пользователя',
                        "cont_name": f'Имя получателя',
                        "cont_status": f'Статус получателя',
                        "cont_adress": f'Адрес получчателя',
                        "cont_phone": f'Телефон получателя',
                        "cont_email": f'Email получателя',
                        "cont_inn": f'ИНН получателя',
                        "cont_pasport": f'Паспорт получателя',
                        "cont_born": f'Дата рождения получателя',
                        "cont_comment": f'Комментарий получателя'}

    dict_oper = {"name": f'{my_card[1]}',
                 "status": f'{my_card[2]}',
                 "adress": f'{my_card[3]}',
                 "phone": f'{my_card[4]}',
                 "email": f'{my_card[5]}',
                 "inn": f'{my_card[6]}',
                        "pasport": f'{my_card[7]}',
                        "born": f'{my_card[8]}',
                        "comment": f'{my_card[9]}',
                        "cont_name": f'{cont_card[0]}',
                        "cont_status": f'{cont_card[1]}',
                        "cont_adress": f'{cont_card[2]}',
                        "cont_phone": f'{cont_card[3]}',
                        "cont_email": f'{cont_card[4]}',
                        "cont_inn": f'{cont_card[5]}',
                        "cont_pasport": f'{cont_card[6]}',
                        "cont_born": f'{cont_card[7]}',
                        "cont_comment": f'{cont_card[8]}'}

    lst_none = []
    for x in Dict_user.dict_user_full_text[f'{call.message.chat.id}']:
        if dict_oper[x] == "":
            lst_none.append(x)
    await state.update_data(
        {
            'dict_oper': dict_oper,
            'lst_none': lst_none
        }
    )
    if len(lst_none) != 0:
        await letter_3(message=call.message, state=state)
    else:
        await letter_3(message=call.message, state=state)


async def letter_3(message: types.Message, state: FSMContext):
    data = await state.get_data()
    dict_oper = data['dict_oper']
    link_template = Dict_user.dict_user_call[f'{message.chat.id}']

    response = urllib.request.urlopen(link_template)
    async with aiohttp.ClientSession() as session:
        async with session.get(link_template) as response:
            if response.status == 200:
                content = await response.read()

                with io.BytesIO(content) as f:
                    doc = docx.Document(f)

                    for oper in Dict_user.dict_user_full_text[f'{message.chat.id}']:
                        for paragraph in doc.paragraphs:
                            text = paragraph.text
                            search_str = f'{{{{{oper}}}}}'
                            paragraph.text = text.replace(
                                search_str, dict_oper[oper])
                    doc.save('modified_output.docx')
                    file = 'modified_output.docx'
                    # convert(file, file[:-5] + ".pdf")
                    command = ['libreoffice', '--convert-to', 'pdf', file]
                    subprocess.run(command, check=True)
                    await bot.send_document(message.chat.id, open('modified_output.pdf', 'rb'))
