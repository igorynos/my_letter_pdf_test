from aiogram.dispatcher.filters.state import StatesGroup, State
# from handlers.users.start import Dict_user
# from loader import dp
# from aiogram.dispatcher.storage import FSMContext
# from aiogram import types


class State_list(StatesGroup):
    Q0 = State()
    Q1 = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()
    Q5 = State()
    Q6 = State()
    Q7 = State()
    Q8 = State()
    Q9 = State()
    Q10 = State()


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
#         Dict_user.dict_user_answer[user_id] = data
#         print(data)
#         await state.finish()


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
#         Dict_user.dict_user_answer[user_id] = data
#         print(data)
#         await state.finish()


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
#         Dict_user.dict_user_answer[user_id] = data
#         print(data)
#         await state.finish()


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
#         Dict_user.dict_user_answer[user_id] = data
#         print(Dict_user.dict_user_answer[user_id])
#         await state.finish()


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
#         Dict_user.dict_user_answer[user_id] = data
#         print(data)
#         await state.finish()


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
#         Dict_user.dict_user_answer[user_id] = data
#         print(data)
#         await state.finish()


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
#         Dict_user.dict_user_answer[user_id] = data
#         print(data)
#         await state.finish()


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
#         Dict_user.dict_user_answer[user_id] = data
#         print(data)
#         await state.finish()


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
#         Dict_user.dict_user_answer[user_id] = data
#         print(data)
#         await state.finish()


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
#         Dict_user.dict_user_answer[user_id] = data
#         print(data)
#         await state.finish()


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
#         Dict_user.dict_user_answer[user_id] = data
#         print(data)
#         await state.finish()
# if __name__ == "__main__":
#     print(State_list.lst_state['Q0'])
