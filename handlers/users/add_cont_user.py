from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from loader import db
from loader import bot

from keyboards.inline.choise_cont_user import dell_choise_cont_user
from keyboards.inline.callback_data import dell_cont_user_choise
from keyboards.inline.choise_cont_user import nest_pars, cont_user, accept_dell
from keyboards.default.menu_start import menu_start_admin, menu_start_user

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from data import config

from dadata import Dadata
import random

dict_temp = {}


@dp.callback_query_handler(text='Удалить получателя')
async def dell_cont_user(call: types.CallbackQuery):
    await dell_choise_cont_user(call.message)


# @dp.message_handler(text='Пропустить', state='*')
# async def miss(call: types.CallbackQuery, state: FSMContext):
#     await bot.send_message(chat_id=call.message.chat.id, text='Пропустить')


@dp.callback_query_handler(dell_cont_user_choise.filter())
async def cont_user_card(call: CallbackQuery, callback_data: dict, state: FSMContext):
    dict_temp[f"{call.message.chat.id}"] = callback_data.get('id')
    await call.message.answer("Вы действтельно хотите удалить пользователя?", reply_markup=accept_dell)


@dp.callback_query_handler(text="dell_yes")
async def cont_user_card_dell_yes(call: CallbackQuery):
    print("YES")
    quantity = dict_temp[f"{call.message.chat.id}"]
    sql = f"DELETE FROM cont_users WHERE id='{quantity}'"
    db.execute(sql, fetchone=True, commit=True)

    await bot.send_message(chat_id=call.message.chat.id, text=f"Получатель удалён", reply_markup=cont_user)


@dp.callback_query_handler(text="dell_no")
async def cont_user_card_dell_no(call: CallbackQuery):
    print("NO")
    dict_temp[f"{call.message.chat.id}"] = ''
    await dell_choise_cont_user(call.message)


@dp.callback_query_handler(text='Добавить получателя')
async def add_cont_user_0(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Напишите ИНН получателя", reply_markup=nest_pars)
    await state.set_state("add_cont_user_1")


@dp.message_handler(state='add_cont_user_1')
async def add_cont_user_1(message: types.Message, state: FSMContext):
    name = message.text
    token = "20473d0a0f63fdc5c6921b0d9b54ae2ca0745429"
    dadata = Dadata(token)
    data = dadata.find_by_id("party", name)

    if data != []:
        company_info = data[0]
        db.add_cont_user(org=company_info['value'],
                         ogrn=company_info['data']['ogrn'],
                         adress=company_info['data']['address']['unrestricted_value'],
                         fio=company_info['data']['management']['name'],
                         headstatus=company_info['data']['management']['post'],
                         inn=name,
                         id=random.randint(1000000, 9999999),
                         user=message.chat.id)
        text = f"Получатель {company_info['value']} создан\n\n\
#{name}\n\
{company_info['value']} (ОГРН: {company_info['data']['ogrn']})\n\
Адрес: {company_info['data']['address']['unrestricted_value']}\n\
Получатель: {company_info['data']['management']['post']} - {company_info['data']['management']['name']}"

        if str(message.chat.id) in config.ADMINS:
            await message.answer(text=text, reply_markup=menu_start_admin)
        else:
            await message.answer(text=text, reply_markup=menu_start_user)
        await state.finish()
    else:
        await state.update_data(
            {
                'inn': name
            }
        )
        await message.answer("Напишите наименование организации получателя")
        await state.set_state("add_cont_user_2")


@dp.message_handler(state='add_cont_user_2')
async def add_cont_user_2(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(
        {
            'org': name
        }
    )
    await message.answer("Напишите ОГРН организации получателя", reply_markup=nest_pars)
    await state.set_state("add_cont_user_4")


@dp.message_handler(state='add_cont_user_4')
async def add_cont_user_4(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(
        {
            'ogrn': name
        }
    )
    await message.answer("Напишите почтовый адрес организации получателя", reply_markup=nest_pars)
    await state.set_state("add_cont_user_5")


@dp.message_handler(state='add_cont_user_5')
async def add_cont_user_5(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(
        {
            'adress': name
        }
    )
    await message.answer("Напишите телефон представителя организации получателя", reply_markup=nest_pars)
    await state.set_state("add_cont_user_6")


@dp.message_handler(state='add_cont_user_6')
async def add_cont_user_6(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(
        {
            'phone': name
        }
    )
    await message.answer("Напишите Email организации получателя", reply_markup=nest_pars)
    await state.set_state("add_cont_user_7")


@dp.message_handler(state='add_cont_user_7')
async def add_cont_user_7(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(
        {
            'email': name
        }
    )
    await message.answer("Напишите ФИО руководителя организации получателя", reply_markup=nest_pars)
    await state.set_state("add_cont_user_8")


@dp.message_handler(state='add_cont_user_8')
async def add_cont_user_8(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(
        {
            'fio': name
        }
    )
    await message.answer("Напишите должность руководителя организации получателя", reply_markup=nest_pars)
    await state.set_state("add_cont_user_9")


@dp.message_handler(state='add_cont_user_9')
async def add_cont_user_9(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(
        {
            'headstatus': name
        }
    )
    await message.answer("Напишите ФИО представителя организации получателя", reply_markup=nest_pars)
    await state.set_state("add_cont_user_10")


@dp.message_handler(state='add_cont_user_10')
async def add_cont_user_10(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(
        {
            'fiocont': name
        }
    )
    await message.answer("Напишите ссылку на организацию получателя", reply_markup=nest_pars)
    await state.set_state("add_cont_user_11")


@dp.message_handler(state='add_cont_user_11')
async def add_cont_user_11(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(
        {
            'link': name
        }
    )
    data = await state.get_data()
    for x in data.keys():
        if data[x] == 'Пропустить':
            data[x] = ''

    db.add_cont_user(org=data["org"],
                     ogrn=data["ogrn"],
                     adress=data["adress"],
                     phone=data["phone"],
                     email=data["email"],
                     inn=data['inn'],
                     fio=data['fio'],
                     headstatus=data['headstatus'],
                     fiocont=data['fiocont'],
                     link=data['link'],
                     id=random.randint(1000000, 9999999),
                     user=message.chat.id)

    text = f"Получатель {data['org']} создан"

    if str(message.chat.id) in config.ADMINS:
        await message.answer(text=text, reply_markup=menu_start_admin)
    else:
        await message.answer(text=text, reply_markup=menu_start_user)
    await state.finish()
