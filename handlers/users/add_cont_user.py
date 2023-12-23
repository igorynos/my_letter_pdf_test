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
from keyboards.inline.choise_cont_user import nest_pars, cont_user
from keyboards.inline.menu_start import menu_start_user, menu_start_admin

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from data import config


@dp.callback_query_handler(text='Удалить получателя')
async def dell_cont_user(call: types.CallbackQuery):
    await dell_choise_cont_user(call.message)


# @dp.message_handler(text='Пропустить', state='*')
# async def miss(call: types.CallbackQuery, state: FSMContext):
#     await bot.send_message(chat_id=call.message.chat.id, text='Пропустить')


@dp.callback_query_handler(dell_cont_user_choise.filter())
async def cont_user_card(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    quantity = callback_data.get('id')
    sql = f"DELETE FROM cont_users WHERE id='{quantity}'"
    db.execute(sql, fetchone=True, commit=True)

    await bot.send_message(chat_id=call.message.chat.id, text=f"Получатель удалён", reply_markup=cont_user)


@dp.callback_query_handler(text='Добавить получателя')
async def add_cont_user_1(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Напишите наименование организации получателя")
    await state.set_state("add_cont_user_2")


@dp.message_handler(state='add_cont_user_2')
async def add_cont_user_2(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(
        {
            'org': name
        }
    )
    await message.answer("Напишите почтовый адрес организации получателя", reply_markup=nest_pars)
    await state.set_state("add_cont_user_4")


@dp.message_handler(state='add_cont_user_4')
async def add_cont_user_4(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(
        {
            'adress': name
        }
    )
    await message.answer("Напишите ФИО руководителя организации получателя", reply_markup=nest_pars)
    await state.set_state("add_cont_user_5")


@dp.message_handler(state='add_cont_user_5')
async def add_cont_user_5(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(
        {
            'fio': name
        }
    )
    await message.answer("Напишите должность руководителя организации получателя", reply_markup=nest_pars)
    await state.set_state("add_cont_user_6")


@dp.message_handler(state='add_cont_user_6')
async def add_cont_user_9(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(
        {
            'headstatus': name
        }
    )
    data = await state.get_data()
    for x in data.keys():
        if data[x] == 'Пропустить':
            data[x] = ''

    db.add_cont_user(org=data["org"],
                     adress=data["adress"],
                     fio=data['fio'],
                     headstatus=data['headstatus'],
                     user=message.chat.id)

    await message.answer(f"Получатель {data['org']} создан", reply_markup=types.ReplyKeyboardRemove())
    if str(message.chat.id) in config.ADMINS:
        await message.answer(f"Выберите действие:", reply_markup=menu_start_admin)
    else:
        await message.answer(f"Выберите действие:", reply_markup=menu_start_user)
    await state.finish()
