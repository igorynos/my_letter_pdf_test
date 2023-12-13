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

from states.letter import State_list

import io

from keyboards.inline.choise_template import choice
from keyboards.inline.choise_template import delete_choice
from keyboards.inline.change_user_card import change_card
from keyboards.inline.choise_cont_user import choise_cont_user, change_cont_card
from keyboards.inline.callback_data import template, del_template, change_my_card, cont_user_choise, change_cont_user_choise

import pymysql

import urllib.request

import docx
import io
import urllib.request
import re
from docx2pdf import convert
import aiohttp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    sql = f"SELECT * FROM users WHERE id = '{message.from_user.id}';"
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
        await message.answer(f"Выберите действие", reply_markup=menu_1)


@dp.message_handler(text='В начало')
async def in_start(message: types.Message, state: FSMContext):
    await bot_start(message=message, state=state)


@dp.message_handler(text='Словарь операндов')
async def dict_oper(message: types.Message):
    text = ('{{name}} - Имя пользователя\n\
{{status}} - Статус пользователя\n\
{{adress}} - Адресс пользователя\n\
{{phone}} - Телефон пользователя\n\
{{email}} - Email пользователя\n\
{{inn}} - ИНН пользователя\n\
{{pasport}} - Пасспорт пользователя\n\
{{born}} - Дата рождения пользователя\n\
{{comment}} - Комментарий пользователя\n\
{{cont_name}} - Имя получателя\n\
{{cont_status}} - Статус получателя\n\
{{cont_adress}} - Адрес получчателя\n\
{{cont_phone}} - Телефон получателя\n\
{{cont_email}} - Email получателя\n\
{{cont_inn}} - ИНН получателя\n\
{{cont_pasport}} - Паспорт получателя\n\
{{cont_born}} - Дата рождения получателя\n\
{{cont_comment}} - Комментарий получателя')
    await message.answer(text=text)


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
    await message.answer(f"Выберите действие", reply_markup=menu_1)


@dp.message_handler(text='Создать письмо')
async def enter_test(message: types.Message):
    await choice(message)


@dp.message_handler(text='Получатели')
async def enter_test(message: types.Message):
    await choise_cont_user(message)


@dp.message_handler(text='Добавить шаблон')
async def new_tamplate(message: types.Message, state: FSMContext):
    await message.answer("Название шаблона")
    await state.set_state("name_tamplate")


@dp.message_handler(text='Шаблоны')
async def tamplates(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text="Выберите действие", reply_markup=menu_template)


@dp.message_handler(text='Удалить шаблон')
async def delete_tamplate(message: types.Message):
    await delete_choice(message)


@dp.message_handler(text='Мои реквизиты')
async def my_user_card(message: types.Message):
    sql = f"SELECT * FROM users WHERE id='{message.chat.id}'"
    my_card = db.execute(sql, fetchall=True, commit=True)
    my_card = my_card[0]

    text = f"Ваши реквизиты:\n\n\
    ФИО: {my_card[1]}\n\
    Статус: {my_card[2]}\n\
    Адрес: {my_card[3]}\n\
    Тел: {my_card[4]}\n\
    Email: {my_card[5]}\n\
    ИНН: {my_card[6]}\n\
    Паспорт: {my_card[7]}\n\
    Дата рождения: {my_card[8]}\n\
    Комментарий: {my_card[9]}"
    await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=user_card)


@dp.callback_query_handler(cont_user_choise.filter())
async def cont_user_card(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    quantity = callback_data.get('name')
    sql = f"SELECT * FROM cont_users WHERE name='{quantity}'"
    my_card = db.execute(sql, fetchall=True, commit=True)
    my_card = my_card[0]

    text = f"Реквизиты получателя:\n\n\
    ФИО: {my_card[0]}\n\
    Статус: {my_card[1]}\n\
    Адрес: {my_card[2]}\n\
    Тел: {my_card[3]}\n\
    Email: {my_card[4]}\n\
    ИНН: {my_card[5]}\n\
    Паспорт: {my_card[6]}\n\
    Дата рождения: {my_card[7]}\n\
    Комментарий: {my_card[8]}"
    await bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=cont_user_2)


@dp.message_handler(text='Изменить')
async def my_user_card_2(message: types.Message):
    await change_card(message)


@dp.message_handler(text='Изменить данные')
async def cont_user_card_2(message: types.Message):
    await change_cont_card(message)


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

    # response = urllib.request.urlopen(link_template)
    # # Открытие потока байтов и создание объекта docx.Document
    # async with aiohttp.ClientSession() as session:
    #     async with session.get(link_template) as response:
    #         if response.status == 200:
    #             content = await response.read()

    #             # Use io.BytesIO to create a bytes stream from content
    #             with io.BytesIO(content) as f:
    #                 doc = docx.Document(f)

    #                 # Continue with your code to process the doc
    #                 full_text = []
    #                 for paragraph in doc.paragraphs:
    #                     if '{{' in paragraph.text:
    #                         text = paragraph.text
    #                         pattern = r'\{\{(.+?)\}\}'
    #                         matches = re.findall(pattern, text)
    #                         full_text.extend(matches)

    db.add_template(name=name, link=link_template, oper='')

    await state.finish()

    await message.answer(text=f'Новый шаблон {name} создан')


@dp.callback_query_handler(del_template.filter())
async def letter(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    quantity = callback_data.get('name')
    sql = f"DELETE FROM template WHERE name = '{quantity}'"
    db.execute(sql, fetchall=True, commit=True)
    await call.message.answer(text=f'Шаблон {quantity} удалён')


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
    quantity = callback_data.get('name')

    await state.update_data(
        {
            f'answer': quantity
        }
    )

    await call.message.answer("Напишите новое значение")
    await state.set_state("change_cont_card_3")


@dp.message_handler(state="change_card_3")
async def change_card_3(message: types.Message, state: FSMContext):
    data = await state.get_data()
    answer1 = data.get("answer")
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

    sql = f"UPDATE users SET {answer1} = '{answer2}' WHERE id = {message.chat.id}"
    db.execute(sql, fetchone=True, commit=True)
    await state.finish()
    await message.answer(f"{dict_column_name[f'{answer1}']}")
    await my_user_card(message)


@dp.message_handler(state="change_cont_card_3")
async def change_cont_card_3(message: types.Message, state: FSMContext):
    data = await state.get_data()
    answer1 = data.get("answer")
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

    sql = f"UPDATE cont_users SET {answer1} = '{answer2}' WHERE user = {message.chat.id}"
    db.execute(sql, fetchone=True, commit=True)
    await state.finish()
    await message.answer(f"{dict_column_name[f'{answer1}']}", reply_markup=cont_user_2)


# @dp.message_handler(text="Письмо создаётся...")
# async def get_pdf(message: types.Message, state: FSMContext):
#     link_template = Dict_user.dict_user_call[f'{message.from_user.id}']

#     response = urllib.request.urlopen(link_template)
#     async with aiohttp.ClientSession() as session:
#         async with session.get(link_template) as response:
#             if response.status == 200:
#                 content = await response.read()

#                 with io.BytesIO(content) as f:
#                     doc = docx.Document(f)

#                     for oper in Dict_user.dict_user_answer[f'{message.from_user.id}'].items():
#                         for paragraph in doc.paragraphs:
#                             text = paragraph.text
#                             search_str = f'{{{{{oper[0]}}}}}'
#                             paragraph.text = text.replace(search_str, oper[1])
#                     doc.save('modified_output.docx')
#                     file = 'modified_output.docx'
#                     convert(file, file[:-5] + ".pdf")
#                     await bot.send_document(message.chat.id, open('modified_output.pdf', 'rb'))


# @dp.message_handler(state=State_list.Q0)
# async def answer_lst(message: types.Message, state: FSMContext):
#     user_id = Dict_user.dict_user_indx[f"{message.from_user.id}"]
#     user_text = Dict_user.dict_user_full_text[f'{message.from_user.id}']

#     answer = message.text

#     await state.update_data(
#         {
#             f'{user_text[user_id]}': answer
#         }
#     )

#     try:
#         Dict_user.dict_user_indx[f"{message.from_user.id}"] += 1
#         await message.answer(f"Напиши {user_text[user_id+1]}")
#         await State_list.next()
#     except:
#         data = await state.get_data()
#         Dict_user.dict_user_answer[f'{message.from_user.id}'] = data
#         await state.finish()
#         await message.answer(text="Письмо создаётся...")
#         await get_pdf(message=message, state=FSMContext)


# @dp.message_handler(state=State_list.Q1)
# async def answer_lst(message: types.Message, state: FSMContext):
#     user_id = Dict_user.dict_user_indx[f"{message.from_user.id}"]
#     user_text = Dict_user.dict_user_full_text[f'{message.from_user.id}']

#     answer = message.text

#     await state.update_data(
#         {
#             f'{user_text[user_id]}': answer
#         }
#     )

#     try:
#         Dict_user.dict_user_indx[f"{message.from_user.id}"] += 1
#         await message.answer(f"Напиши {user_text[user_id+1]}")
#         await State_list.next()
#     except:
#         data = await state.get_data()
#         Dict_user.dict_user_answer[f'{message.from_user.id}'] = data
#         await state.finish()
#         await message.answer(text="Письмо создаётся...")
#         await get_pdf(message=message, state=FSMContext)


# @dp.message_handler(state=State_list.Q2)
# async def answer_lst(message: types.Message, state: FSMContext):
#     user_id = Dict_user.dict_user_indx[f"{message.from_user.id}"]
#     user_text = Dict_user.dict_user_full_text[f'{message.from_user.id}']

#     answer = message.text

#     await state.update_data(
#         {
#             f'{user_text[user_id]}': answer
#         }
#     )

#     try:
#         Dict_user.dict_user_indx[f"{message.from_user.id}"] += 1
#         await message.answer(f"Напиши {user_text[user_id+1]}")
#         await State_list.next()
#     except:
#         data = await state.get_data()
#         Dict_user.dict_user_answer[f'{message.from_user.id}'] = data
#         await state.finish()
#         await message.answer(text="Письмо создаётся...")
#         await get_pdf(message=message, state=FSMContext)


# @dp.message_handler(state=State_list.Q3)
# async def answer_lst(message: types.Message, state: FSMContext):
#     user_id = Dict_user.dict_user_indx[f"{message.from_user.id}"]
#     user_text = Dict_user.dict_user_full_text[f'{message.from_user.id}']

#     answer = message.text

#     await state.update_data(
#         {
#             f'{user_text[user_id]}': answer
#         }
#     )

#     try:
#         Dict_user.dict_user_indx[f"{message.from_user.id}"] += 1
#         await message.answer(f"Напиши {user_text[user_id+1]}")
#         await State_list.next()
#     except:
#         data = await state.get_data()
#         Dict_user.dict_user_answer[f'{message.from_user.id}'] = data
#         await state.finish()
#         await message.answer(text="Письмо создаётся...")
#         await get_pdf(message=message, state=FSMContext)


# @dp.message_handler(state=State_list.Q4)
# async def answer_lst(message: types.Message, state: FSMContext):
#     user_id = Dict_user.dict_user_indx[f"{message.from_user.id}"]
#     user_text = Dict_user.dict_user_full_text[f'{message.from_user.id}']

#     answer = message.text

#     await state.update_data(
#         {
#             f'{user_text[user_id]}': answer
#         }
#     )

#     try:
#         Dict_user.dict_user_indx[f"{message.from_user.id}"] += 1
#         await message.answer(f"Напиши {user_text[user_id+1]}")
#         await State_list.next()
#     except:
#         data = await state.get_data()
#         Dict_user.dict_user_answer[f'{message.from_user.id}'] = data
#         await state.finish()
#         await message.answer(text="Письмо создаётся...")
#         await get_pdf(message=message, state=FSMContext)


# @dp.message_handler(state=State_list.Q5)
# async def answer_lst(message: types.Message, state: FSMContext):
#     user_id = Dict_user.dict_user_indx[f"{message.from_user.id}"]
#     user_text = Dict_user.dict_user_full_text[f'{message.from_user.id}']

#     answer = message.text

#     await state.update_data(
#         {
#             f'{user_text[user_id]}': answer
#         }
#     )

#     try:
#         Dict_user.dict_user_indx[f"{message.from_user.id}"] += 1
#         await message.answer(f"Напиши {user_text[user_id+1]}")
#         await State_list.next()
#     except:
#         data = await state.get_data()
#         Dict_user.dict_user_answer[f'{message.from_user.id}'] = data
#         await state.finish()
#         await message.answer(text="Письмо создаётся...")
#         await get_pdf(message=message, state=FSMContext)


# @dp.message_handler(state=State_list.Q6)
# async def answer_lst(message: types.Message, state: FSMContext):
#     user_id = Dict_user.dict_user_indx[f"{message.from_user.id}"]
#     user_text = Dict_user.dict_user_full_text[f'{message.from_user.id}']

#     answer = message.text

#     await state.update_data(
#         {
#             f'{user_text[user_id]}': answer
#         }
#     )

#     try:
#         Dict_user.dict_user_indx[f"{message.from_user.id}"] += 1
#         await message.answer(f"Напиши {user_text[user_id+1]}")
#         await State_list.next()
#     except:
#         data = await state.get_data()
#         Dict_user.dict_user_answer[f'{message.from_user.id}'] = data
#         await state.finish()
#         await message.answer(text="Письмо создаётся...")
#         await get_pdf(message=message, state=FSMContext)


# @dp.message_handler(state=State_list.Q7)
# async def answer_lst(message: types.Message, state: FSMContext):
#     user_id = Dict_user.dict_user_indx[f"{message.from_user.id}"]
#     user_text = Dict_user.dict_user_full_text[f'{message.from_user.id}']

#     answer = message.text

#     await state.update_data(
#         {
#             f'{user_text[user_id]}': answer
#         }
#     )

#     try:
#         Dict_user.dict_user_indx[f"{message.from_user.id}"] += 1
#         await message.answer(f"Напиши {user_text[user_id+1]}")
#         await State_list.next()
#     except:
#         data = await state.get_data()
#         Dict_user.dict_user_answer[f'{message.from_user.id}'] = data
#         await state.finish()
#         await message.answer(text="Письмо создаётся...")
#         await get_pdf(message=message, state=FSMContext)


# @dp.message_handler(state=State_list.Q8)
# async def answer_lst(message: types.Message, state: FSMContext):
#     user_id = Dict_user.dict_user_indx[f"{message.from_user.id}"]
#     user_text = Dict_user.dict_user_full_text[f'{message.from_user.id}']

#     answer = message.text

#     await state.update_data(
#         {
#             f'{user_text[user_id]}': answer
#         }
#     )

#     try:
#         Dict_user.dict_user_indx[f"{message.from_user.id}"] += 1
#         await message.answer(f"Напиши {user_text[user_id+1]}")
#         await State_list.next()
#     except:
#         data = await state.get_data()
#         Dict_user.dict_user_answer[f'{message.from_user.id}'] = data
#         await state.finish()
#         await message.answer(text="Письмо создаётся...")
#         await get_pdf(message=message, state=FSMContext)


# @dp.message_handler(state=State_list.Q9)
# async def answer_lst(message: types.Message, state: FSMContext):
#     user_id = Dict_user.dict_user_indx[f"{message.from_user.id}"]
#     user_text = Dict_user.dict_user_full_text[f'{message.from_user.id}']

#     answer = message.text

#     await state.update_data(
#         {
#             f'{user_text[user_id]}': answer
#         }
#     )

#     try:
#         Dict_user.dict_user_indx[f"{message.from_user.id}"] += 1
#         await message.answer(f"Напиши {user_text[user_id+1]}")
#         await State_list.next()
#     except:
#         data = await state.get_data()
#         Dict_user.dict_user_answer[f'{message.from_user.id}'] = data
#         await state.finish()
#         await message.answer(text="Письмо создаётся...")
#         await get_pdf(message=message, state=FSMContext)


# @dp.message_handler(state=State_list.Q10)
# async def answer_lst(message: types.Message, state: FSMContext):
#     user_id = Dict_user.dict_user_indx[f"{message.from_user.id}"]
#     user_text = Dict_user.dict_user_full_text[f'{message.from_user.id}']

#     answer = message.text

#     await state.update_data(
#         {
#             f'{user_text[user_id]}': answer
#         }
#     )

#     try:
#         Dict_user.dict_user_indx[f"{message.from_user.id}"] += 1
#         await message.answer(f"Напиши {user_text[user_id+1]}")
#         await State_list.next()
#     except:
#         data = await state.get_data()
#         Dict_user.dict_user_answer[f'{message.from_user.id}'] = data
#         await state.finish()
#         await message.answer(text="Письмо создаётся...")
#         await get_pdf(message=message, state=FSMContext)
