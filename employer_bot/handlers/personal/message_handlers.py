from aiogram import types
from main import dp, bot
from config import date_pattern, time_pattern
from requests_db import *
from fsm import *
from keyboard import *
import re


########################################
# Callback handlers / Обрабочтики кнопок
########################################


@dp.callback_query_handler(lambda call: call.data == '/reg_admin')
async def reg_admin(callback_query: types.CallbackQuery):
    global owner_message_bot
    owner_message_bot = await owner_message_bot.edit_text('Введите свое ФИО')
    await Registration().role_user.set()
    await callback_query.answer()

"""
@dp.callback_query_handler(lambda call: call.data == '/check_task')
async def check_task(callback_query: types.CallbackQuery):
    global owner_message_bot
    all_task = select_all_task()
    if all_task:
        list_task = []
        for task in all_task:
            if task[1] == 'global':
                list_task.append(
                    f'Название задачи: {task[2]}\nОписание задачи: {task[3]}\nДедлайн задачи: {task[4]}\nИсполнитель: бригада - {task[6]}\n\n')
                print(list_task)
            elif task[1] == 'project':
                list_task.append(
                    f'Название задачи: {task[2]}\nОписание задачи: {task[3]}\nДедлайн задачи: {task[4]}\nИсполнитель: проект - {task[6]}\n\n')
            elif task[1] == 'mini':
                list_task.append(
                    f'Название задачи: {task[2]}\nДедлайн задачи: {task[4]}\nИсполнитель: сотрудник - {task[6]}\n\n')
        list_task = '\n'.join(list_task)
        owner_message_bot = await owner_message_bot.edit_text(f'Ваши задачи:\n\n{list_task}\n\nЧтобы отметить задачу выполненной, пришлите ее название')
        owner_message_bot = await owner_message_bot.edit_reply_markup(markup_cancel)
        await Done_task.name_task.set()
        await callback_query.answer()
    else:
        owner_message_bot = await owner_message_bot.edit_text('У вас нету задач')
        owner_message_bot = await owner_message_bot.edit_reply_markup(markup_menu)"""


@dp.callback_query_handler(lambda call: call.data == '/check_task')
async def check_task(callback_query: types.CallbackQuery):
    global owner_message_bot
    user_id = select_id_user(f'@{callback_query.from_user.username}')
    print(user_id)
    project_user_task = get_project_user(user_id[0])
    print(project_user_task)
    user_task = select_user_task(f'@{callback_query.from_user.username}')
    if project_user_task or user_task:
        list_project = []
        for project in project_user_task:
            project_task = select_task_for_project(project[0])
            print(project_task)
            for task in project_task:
                print(task)
                list_project.append(
                    f'Название задачи: {task[2]}\nОписание задачи: {task[3]}\nДедлайн задачи: {task[4]}\nИсполнитель: проект - {task[6]}\n\n')
        for task in user_task:
            list_project.append(
                f'Название задачи: {task[2]}\nДедлайн задачи: {task[4]}\nИсполнитель: сотрудник - {task[6]}\n\n')
        list_project = '\n'.join(list_project)
        owner_message_bot = await owner_message_bot.edit_text(f'Ваши задачи:\n\n{list_project}\n\nЧтобы отметить задачу выполненной, пришлите ее название')
        owner_message_bot = await owner_message_bot.edit_reply_markup(markup_cancel)
    else:
        owner_message_bot = await owner_message_bot.edit_text('У вас нету задач')
        owner_message_bot = await owner_message_bot.edit_reply_markup(markup_menu)


@dp.callback_query_handler(lambda call: call.data == '/cancel', state='*')
async def cancel(callback_query: types.CallbackQuery, state: FSMContext):
    global owner_message_bot
    owner_message_bot = await owner_message_bot.edit_text('Главное меню')
    owner_message_bot = await owner_message_bot.edit_reply_markup(markup_menu)
    await state.reset_data()
    await state.reset_state()
    await state.finish()
    await callback_query.answer()


##########################################
# Message handlers / Обрабочтики сообщений
##########################################


@dp.message_handler(commands='start')
async def command_start(message: types.Message):
    global owner_message_bot
    user = select_id_user(f'@{message.from_user.username}')
    if not user:
        owner_message_bot = await bot.send_message(message.chat.id, f'@{message.from_user.username}, приветствую. Пройди простую регистрацию', reply_markup=markup_reg)
        await message.delete()
    else:
        owner_message_bot = await bot.send_message(message.chat.id, 'Вы уже зарегистрированы', reply_markup=markup_brigade)
        await message.delete()


@dp.message_handler(commands='menu')
async def command_menu(message: types.Message):
    global owner_message_bot
    user = select_id_user(f'@{message.from_user.username}')
    if user:
        owner_message_bot = await bot.send_message(message.chat.id, 'Главное меню', reply_markup=markup_brigade)
        await message.delete()
    else:
        owner_message_bot = await bot.send_message(message.chat.id, 'Вы не зарегистрированы', reply_markup=markup_reg)


@dp.message_handler(state=Registration.role_user)
async def write_firstName(message: types.Message, state: FSMContext):
    await message.delete()
    await state.update_data(role_user='user')
    await Registration.next()
    await state.update_data(name=message.text)
    await Registration.next()
    await state.update_data(tag_telegram=f'@{message.from_user.username}')
    data_user = await state.get_data()
    global owner_message_bot
    owner_message_bot = await owner_message_bot.edit_text('Отлично, вы зарегистрировались')
    await owner_message_bot.edit_reply_markup(markup_menu)
    add_user(data_user['role_user'], data_user['name'],
             data_user['tag_telegram'])
    await state.finish()


@dp.message_handler(state=Done_task.name_task)
async def done_task(message: types.Message, state: FSMContext):
    await message.delete()
    global owner_message_bot
    if select_one_task(message.text):
        await state.update_data(name_task=message.text)
        change_status_task(message.text)
        owner_message_bot = await owner_message_bot.edit_text(f'Задача {message.text} отмечена выполненной')
        owner_message_bot = await owner_message_bot.edit_reply_markup(markup_menu)
        await state.finish()
    else:
        owner_message_bot = await owner_message_bot.edit_text('Такой задачи нету в списке, повторите ввод')
        owner_message_bot = await owner_message_bot.edit_reply_markup(markup_cancel)
