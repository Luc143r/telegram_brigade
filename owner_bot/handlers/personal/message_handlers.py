from aiogram import types
from main import dp, bot
from requests_db import *
from fsm import *
from keyboard import *


########################################
# Callback handlers / Обрабочтики кнопок
########################################


@dp.callback_query_handler(text='/reg_admin')
async def reg_admin(callback_query: types.CallbackQuery):
    global owner_message_bot
    owner_message_bot = await owner_message_bot.edit_text('Введите свое ФИО')
    await Registration().role_user.set()
    callback_query.answer()


@dp.callback_query_handler(text='/main_menu')
async def send_menu(callback_query: types.CallbackQuery):
    global owner_message_bot
    owner_message_bot = await owner_message_bot.edit_text('Главное меню')
    owner_message_bot = await owner_message_bot.edit_reply_markup(markup_brigade)
    callback_query.answer()


@dp.callback_query_handler(text='/add_brigade')
async def add_brigade_menu(callback_query: types.CallbackQuery):
    global owner_message_bot
    owner_message_bot = await owner_message_bot.edit_text('Введите название бригады')
    await Add_brigade().name_brigade.set()
    callback_query.answer()


@dp.callback_query_handler(text='/list_brigade')
async def send_list_brigade(callback_query: types.CallbackQuery):
    global owner_message_bot
    all_brigade = select_all_brigade()
    if all_brigade:
        list_brigade = []
        for brigade in all_brigade:
            list_brigade.append(
                f'Название бригады: {brigade[1]} || Ответственный сотрудник: {brigade[2]}')
        list_brigade = '\n'.join(list_brigade)
        owner_message_bot = await owner_message_bot.edit_text(f'Ваши бригады\n\n{list_brigade}')
        owner_message_bot = await owner_message_bot.edit_reply_markup(markup_menu)
        callback_query.answer()
    else:
        owner_message_bot = await owner_message_bot.edit_text('Вы еще не создавали бригад')
        owner_message_bot = await owner_message_bot.edit_reply_markup(markup_menu)
        callback_query.answer()


@dp.callback_query_handler(text='/del_brigade')
async def delete_brigade(callback_query: types.CallbackQuery):
    global owner_message_bot
    all_brigade = select_all_brigade()
    if all_brigade:
        list_brigade = []
        for brigade in all_brigade:
            list_brigade.append(
                f'Название бригады: {brigade[1]} || Ответственный сотрудник: {brigade[2]}')
        list_brigade = '\n'.join(list_brigade)
        owner_message_bot = await owner_message_bot.edit_text(f'Ваши бригады\n\n{list_brigade}\n\nПришлите название бригады, которую хотите удалить')
        await Del_brigade().name_brigade.set()
        callback_query.answer()
    else:
        owner_message_bot = await owner_message_bot.edit_text('У вас нету бригад')
        owner_message_bot = await owner_message_bot.edit_reply_markup(markup_menu)
        callback_query.answer()


@dp.callback_query_handler(text='/add_project')
async def add_proj(callback_query: types.CallbackQuery):
    global owner_message_bot
    all_brigade = select_all_brigade()
    if all_brigade:
        list_brigade = []
        for brigade in all_brigade:
            list_brigade.append(
                f'Название бригады: {brigade[1]} || Ответственный сотрудник: {brigade[2]}')
        list_brigade = '\n'.join(list_brigade)
        owner_message_bot = await owner_message_bot.edit_text(f'Ваши бригады\n\n{list_brigade}\n\nПришлите название бригады, для которой хотите создать проект')
        await Add_project().brigade.set()
        callback_query.answer()
    else:
        owner_message_bot = await owner_message_bot.edit_text('У вас нету бригад, для которых можно было бы создать проект')
        owner_message_bot = await owner_message_bot.edit_reply_markup(markup_menu)
        callback_query.answer()


@dp.callback_query_handler(text='/check_project')
async def list_project(callback_query: types.CallbackQuery):
    global owner_message_bot
    all_project = select_all_project()
    if all_project:
        list_project = []
        for project in all_project:
            list_project.append(
                f'Название бригады: {project[3]} || Название проекта: {project[1]}')
        list_project = '\n'.join(list_project)
        owner_message_bot = await owner_message_bot.edit_text(f'Ваши проекты\n\n{list_project}')
        owner_message_bot = await owner_message_bot.edit_reply_markup(markup_menu)
        callback_query.answer()
    else:
        owner_message_bot = await owner_message_bot.edit_text('Вы еще не создавали проектов')
        owner_message_bot = await owner_message_bot.edit_reply_markup(markup_menu)
        callback_query.answer()


##########################################
# Message handlers / Обрабочтики сообщений
##########################################


@dp.message_handler(commands='start')
async def command_start(message: types.Message):
    global owner_message_bot
    owner_message_bot = await bot.send_message(message.chat.id, f'@{message.from_user.username}, приветствую. Пройди простую регистрацию', reply_markup=markup_reg)
    await message.delete()


@dp.message_handler(commands='reg')
async def command_reg(message: types.Message):
    global owner_message_bot
    owner_message_bot = await bot.send_message(message.chat.id, f'@{message.from_user.username}, приветствую. Пройди простую регистрацию в зависимости от твоей роли в организации', reply_markup=markup_reg)
    await message.delete()


@dp.message_handler(commands='menu')
async def command_menu(message: types.Message):
    global owner_message_bot
    owner_message_bot = await bot.send_message(message.chat.id, 'Главное меню', reply_markup=markup_brigade)
    await message.delete()


@dp.message_handler(state=Registration.role_user)
async def write_firstName(message: types.Message, state: FSMContext):
    await message.delete()
    await state.update_data(role_user='owner')
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


@dp.message_handler(state=Add_brigade.name_brigade)
async def write_nameBrigade(message: types.Message, state: FSMContext):
    await message.delete()
    await state.update_data(name_brigade=message.text)
    global owner_message_bot
    all_user = select_all_user()
    list_users = []
    for user in all_user:
        list_users.append(f'{user[2]} - {user[3]}')
    list_users = '\n'.join(list_users)
    owner_message_bot = await owner_message_bot.edit_text(f'{list_users}\n\nВыберите одного сотрудника из вышеперечисленных и пришлите его тег')

    await Add_brigade.next()


@dp.message_handler(state=Add_brigade.responsible_employer)
async def write_responsibleEmployer(message: types.Message, state: FSMContext):
    await message.delete()
    await state.update_data(responsible_employer=message.text)
    global owner_message_bot
    owner_message_bot = await owner_message_bot.edit_text('Готово, бригада создана')
    owner_message_bot = await owner_message_bot.edit_reply_markup(markup_menu)
    data_brigade = await state.get_data()
    add_brigade(data_brigade['name_brigade'],
                data_brigade['responsible_employer'])
    change_role_user('admin', data_brigade['responsible_employer'])
    change_visible('0', data_brigade['responsible_employer'])
    await state.finish()


@dp.message_handler(state=Del_brigade.name_brigade)
async def delete_one_brigade(message: types.Message, state: FSMContext):
    await message.delete()
    await state.update_data(name_brigade=message.text)
    global owner_message_bot
    responsible_employer = select_one_brigade(message.text)[2]
    del_brig(message.text)
    change_role_user('user', responsible_employer)
    change_visible('1', responsible_employer)
    owner_message_bot = await owner_message_bot.edit_text('Бригада удалена')
    owner_message_bot = await owner_message_bot.edit_reply_markup(markup_menu)
    await state.finish()


@dp.message_handler(state=Add_project.brigade)
async def add_brigade_project(message: types.Message, state: FSMContext):
    await message.delete()
    await state.update_data(brigade=message.text)
    global owner_message_bot
    owner_message_bot = await owner_message_bot.edit_text('Введите название проекта')
    await Add_project.next()


@dp.message_handler(state=Add_project.name_project)
async def add_name_project(message: types.Message, state: FSMContext):
    await message.delete()
    await state.update_data(name_project=message.text)
    global owner_message_bot
    all_users = select_all_user()
    if all_users:
        list_users = []
        for user in all_users:
            list_users.append(f'{user[2]} - {user[3]}')
        list_users = '\n'.join(list_users)
        owner_message_bot = await owner_message_bot.edit_text(f'Доступные сотрудники:\n{list_users}\n\nПришлите список тегов сотрудников, которых хотите добавить в проект одним сообщением')
        await Add_project.next()


@dp.message_handler(state=Add_project.employers)
async def add_employers_project(message: types.Message, state: FSMContext):
    await message.delete()
    await state.update_data(employers=message.text)
    global owner_message_bot
    owner_message_bot = await owner_message_bot.edit_text('Проект успешно добавлен для бригады')
    owner_message_bot = await owner_message_bot.edit_reply_markup(markup_menu)
    info_project = await state.get_data()
    employers = info_project['employers']
    if employers.__contains__('\n'):
        employers = employers.split('\n')
    elif employers.__contains__(','):
        employers = employers.split(',')
    elif employers.__contains__(' '):
        employers = employers.split(' ')
    list_id_employers = []
    for employer in employers:
        id_user = select_id_user(employer.replace(' ', ''))
        if id_user:
            list_id_employers.append(id_user[0])
    add_project(info_project['name_project'], str(
        list_id_employers), info_project['brigade'])
    for user in employers:
        change_visible('0', user.replace(' ', ''))
    await state.finish()
