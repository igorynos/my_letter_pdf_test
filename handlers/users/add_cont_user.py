from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.cont_user import cont_user_2, nest_pars, cont_user


from loader import dp
from loader import db
from loader import bot

from keyboards.inline.choise_cont_user import choise_cont_user, change_cont_card, dell_choise_cont_user
from keyboards.inline.callback_data import change_cont_user_choise, dell_cont_user_choise


@dp.message_handler(text='Удалить получателя')
async def dell_cont_user(message: types.Message):
    await dell_choise_cont_user(message)


@dp.callback_query_handler(dell_cont_user_choise.filter())
async def cont_user_card(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    quantity = callback_data.get('name')
    sql = f"DELETE FROM cont_users WHERE name='{quantity}'"
    db.execute(sql, fetchone=True, commit=True)

    await bot.send_message(chat_id=call.message.chat.id, text=f"Получатель {quantity} удалён", reply_markup=cont_user)


@dp.message_handler(text='Добавить получателя')
async def add_cont_user_1(message: types.Message, state: FSMContext):
    await message.answer("Напиши его ФИО", reply_markup=nest_pars)
    await state.set_state("add_cont_user_2")


@dp.message_handler(state='add_cont_user_2')
async def add_cont_user_2(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(
        {
            'name': name
        }
    )
    await message.answer("Напиши его статус", reply_markup=nest_pars)
    await state.set_state("add_cont_user_3")


@dp.message_handler(state='add_cont_user_3')
async def add_cont_user_3(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(
        {
            'status': name
        }
    )
    await message.answer("Напиши его адрес", reply_markup=nest_pars)
    await state.set_state("add_cont_user_4")


@dp.message_handler(state='add_cont_user_4')
async def add_cont_user_4(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(
        {
            'adress': name
        }
    )
    await message.answer("Напиши его телефон", reply_markup=nest_pars)
    await state.set_state("add_cont_user_5")


@dp.message_handler(state='add_cont_user_5')
async def add_cont_user_5(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(
        {
            'phone': name
        }
    )
    await message.answer("Напиши его email", reply_markup=nest_pars)
    await state.set_state("add_cont_user_6")


@dp.message_handler(state='add_cont_user_6')
async def add_cont_user_6(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(
        {
            'email': name
        }
    )
    await message.answer("Напиши его ИНН", reply_markup=nest_pars)
    await state.set_state("add_cont_user_7")


@dp.message_handler(state='add_cont_user_7')
async def add_cont_user_7(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(
        {
            'inn': name
        }
    )
    await message.answer("Напиши его поспорт", reply_markup=nest_pars)
    await state.set_state("add_cont_user_8")


@dp.message_handler(state='add_cont_user_8')
async def add_cont_user_8(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(
        {
            'pasport': name
        }
    )
    await message.answer("Напиши его дату рождения", reply_markup=nest_pars)
    await state.set_state("add_cont_user_9")


@dp.message_handler(state='add_cont_user_9')
async def add_cont_user_9(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(
        {
            'born': name
        }
    )
    data = await state.get_data()
    for x in data.keys():
        if data[x] == 'Пропустить':
            data[x] = ''

    db.add_cont_user(name=data["name"],
                     status=data["status"],
                     adress=data["adress"],
                     phone=data["phone"],
                     email=data["email"],
                     inn=data["inn"],
                     pasport=data["pasport"],
                     born=data["born"],
                     user=message.chat.id)

    await message.answer(f"Получатель {data['name']} создан", reply_markup=cont_user)
    await state.finish()
