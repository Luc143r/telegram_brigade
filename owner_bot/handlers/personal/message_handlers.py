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


@dp.callback_query_handler(lambda call: call.data == '/main_menu')
async def send_menu(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    global owner_message_bot
    owner_message_bot = await owner_message_bot.edit_text('Главное меню')
    owner_message_bot = await owner_message_bot.edit_reply_markup(markup_brigade)
    await callback_query.answer()


@dp.callback_query_handler(lambda call: call.data == '/add_brigade')
async def add_brigade_menu(callback_query: types.CallbackQuery):
    global owner_message_bot
    owner_message_bot = await owner_message_bot.edit_text('Введите название бригады')
    owner_message_bot = await owner_message_bot.edit_reply_markup(markup_cancel)
    await Add_brigade().name_brigade.set()
    await callback_query.answer()


@dp.callback_query_handler(lambda call: call.data == '/list_brigade')
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
        await callback_query.answer()
    else:
        owner_message_bot = await owner_message_bot.edit_text('Вы еще не создавали бригад')
        owner_message_bot = await owner_message_bot.edit_reply_markup(markup_menu)
        await callback_query.answer()


@dp.callback_query_handler(lambda call: call.data == '/del_brigade')
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
        owner_message_bot = await owner_message_bot.edit_reply_markup(markup_cancel)
        await Del_brigade().name_brigade.set()
        await callback_query.answer()
    else:
        owner_message_bot = await owner_message_bot.edit_text('У вас нету бригад')
        owner_message_bot = await owner_message_bot.edit_reply_markup(markup_menu)
        await callback_query.answer()


@dp.callback_query_handler(lambda call: call.data == '/add_project')
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
        owner_message_bot = await owner_message_bot.edit_reply_markup(markup_cancel)
        await Add_project().brigade.set()
        await callback_query.answer()
    else:
        owner_message_bot = await owner_message_bot.edit_text('У вас нету бригад, для которых можно было бы создать проект')
        owner_message_bot = await owner_message_bot.edit_reply_markup(markup_menu)
        await callback_query.answer()


@dp.callback_query_handler(lambda call: call.data == '/add_global_task')
async def add_global_task(callback_query: types.CallbackQuery):
    global owner_message_bot
    all_brigade = select_all_brigade()
    if all_brigade:
        list_brigade = []
        for brigade in all_brigade:
            list_brigade.append(
                f'Название бригады: {brigade[1]} || Ответственный сотрудник: {brigade[2]}')
        list_brigade = '\n'.join(list_brigade)
        owner_message_bot = await owner_message_bot.edit_text(f'Ваши бригады\n\n{list_brigade}\n\nПришлите название бригады, для которой хотите создать задачу')
        owner_message_bot = await owner_message_bot.edit_reply_markup(markup_cancel)
        await Add_global_task().executor.set()
        await callback_query.answer()
    else:
        owner_message_bot = await owner_message_bot.edit_text('У вас нету бригад, которым можно было бы поставить задачу.')
        owner_message_bot = await owner_message_bot.edit_reply_markup(markup_menu)
        await callback_query.answer()


@dp.callback_query_handler(lambda call: call.data == '/add_project_task')
async def add_project_task(callback_query: types.CallbackQuery):
    global owner_message_bot
    all_project = select_all_project()
    if all_project:
        list_project = []
        for project in all_project:
            list_project.append(f'Название бригады: {project[3]} || Название проекта: {project[1]}')
        list_project = '\n'.join(list_project)
        owner_message_bot = await owner_message_bot.edit_text(f'Ваши проекты\n\n{list_project}\n\nПришлите название проекта, для которого хотите создать задачу')
        owner_message_bot = await owner_message_bot.edit_reply_markup(markup_cancel)
        await Add_project_task().executor.set()
        await callback_query.answer()
    else:
        owner_message_bot = await owner_message_bot.edit_text('У вас нету проектов, которым можно создать задачу')
        owner_message_bot = await owner_message_bot.edit_reply_markup(markup_menu)


@dp.callback_query_handler(lambda call: call.data == '/add_mini_task')
async def add_mini_task(callback_query: types.CallbackQuery):
    global owner_message_bot
    all_user = select_employer()
    if all_user:
        list_user = []
        for user in all_user:
            list_user.append(f'Сотрудник: {user[2]} || Тег сотрудника: {user[3]}')
        list_user = '\n'.join(list_user)
        owner_message_bot = await owner_message_bot.edit_text(f'Ваши сотрудники\n\n{list_user}\n\nПришлите тег сотрудника, которому хотите поставить задачу')
        owner_message_bot = await owner_message_bot.edit_reply_markup(markup_cancel)
        await Add_mini_task.executor.set()
        await callback_query.answer()
    else:
        owner_message_bot = await owner_message_bot.edit_text('У вас нету сотрудников, которым можно поставить задачу')
        owner_message_bot = await owner_message_bot.edit_reply_markup(markup_menu)


@dp.callback_query_handler(lambda call: call.data == '/check_project')
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
        await callback_query.answer()
    else:
        owner_message_bot = await owner_message_bot.edit_text('Вы еще не создавали проектов')
        owner_message_bot = await owner_message_bot.edit_reply_markup(markup_menu)
        await callback_query.answer()


@dp.callback_query_handler(lambda call: call.data == '/del_project')
async def delete_project(callback_query: types.CallbackQuery):
    global owner_message_bot
    all_project = select_all_project()
    if all_project:
        list_project = []
        for project in all_project:
            list_project.append(
                f'Название бригады: {project[3]} || Ответственный сотрудник: {project[1]}')
        list_project = '\n'.join(list_project)
        owner_message_bot = await owner_message_bot.edit_text(f'Ваши проекты\n\n{list_project}\n\nПришлите название проекта, который хотите удалить')
        owner_message_bot = await owner_message_bot.edit_reply_markup(markup_cancel)
        await Del_project().name_project.set()
        await callback_query.answer()
    else:
        owner_message_bot = await owner_message_bot.edit_text('У вас нету проектов')
        owner_message_bot = await owner_message_bot.edit_reply_markup(markup_menu)
        await callback_query.answer()


@dp.callback_query_handler(lambda call: call.data == '/del_task')
async def delete_task(callback_query: types.CallbackQuery):
    global owner_message_bot
    all_task = select_all_task()
    if all_task:
        list_task = []
        for task in all_task:
            if task[1] == 'global':
                list_task.append(f'Название задачи: {task[2]}\nОписание задачи: {task[3]}\nДедлайн задачи: {task[4]}\nИсполнитель: бригада - {task[6]}\n\n')
                print(list_task)
            elif task[1] == 'project':
                list_task.append(f'Название задачи: {task[2]}\nОписание задачи: {task[3]}\nДедлайн задачи: {task[4]}\nИсполнитель: проект - {task[6]}\n\n')
            elif task[1] == 'mini':
                list_task.append(f'Название задачи: {task[2]}\nДедлайн задачи: {task[4]}\nИсполнитель: сотрудник - {task[6]}\n\n')
        list_task = '\n'.join(list_task)
        owner_message_bot = await owner_message_bot.edit_text(f'Ваши задачи:\n\n{list_task}\n\nПришлите название задачи, которую хотите удалить')
        owner_message_bot = await owner_message_bot.edit_reply_markup(markup_cancel)
        await Del_task.name_task.set()
        await callback_query.answer()
    else:
        owner_message_bot = await owner_message_bot.edit_text('У вас нету задач')
        owner_message_bot = await owner_message_bot.edit_reply_markup(markup_menu)


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


@dp.callback_query_handler(lambda call: call.data == '/cancel_alert')
async def cancel_alert(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await callback_query.answer()


@dp.callback_query_handler(lambda call: call.data == '/cancel', state='*')
async def cancel(callback_query: types.CallbackQuery, state: FSMContext):
    global owner_message_bot
    owner_message_bot = await owner_message_bot.edit_text('Главное меню')
    owner_message_bot = await owner_message_bot.edit_reply_markup(markup_brigade)
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
    owner_message_bot = await owner_message_bot.edit_reply_markup(markup_cancel)

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
    owner_message_bot = await owner_message_bot.edit_reply_markup(markup_cancel)
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
        owner_message_bot = await owner_message_bot.edit_reply_markup(markup_cancel)
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


@dp.message_handler(state=Del_project.name_project)
async def delete_one_brigade(message: types.Message, state: FSMContext):
    await message.delete()
    await state.update_data(name_brigade=message.text)
    global owner_message_bot
    list_employers = select_one_project(message.text)
    for user in list_employers:
        tag_user = get_tag_user(user)
        change_visible(1, tag_user)
    del_proj(message.text)
    owner_message_bot = await owner_message_bot.edit_text('Проект удален')
    owner_message_bot = await owner_message_bot.edit_reply_markup(markup_menu)
    await state.finish()


@dp.message_handler(state=Add_global_task.executor)
async def add_executor_global_task(message: types.Message, state: FSMContext):
    await message.delete()
    brigade = select_one_brigade(message.text)
    global owner_message_bot
    if brigade:
        await state.update_data(executor=message.text)
        owner_message_bot = await owner_message_bot.edit_text('Введите название задачи')
        owner_message_bot = await owner_message_bot.edit_reply_markup(markup_cancel)
        await Add_global_task.next()
    else:
        owner_message_bot = await owner_message_bot.edit_text('Такой бригады нету, повторите ввод заного')
        owner_message_bot = await owner_message_bot.edit_reply_markup(markup_cancel)


@dp.message_handler(state=Add_global_task.name_task)
async def add_name_global_task(message: types.Message, state: FSMContext):
    await message.delete()
    await state.update_data(name_task=message.text)
    global owner_message_bot
    owner_message_bot = await owner_message_bot.edit_text('Введите описание задачи')
    owner_message_bot = await owner_message_bot.edit_reply_markup(markup_cancel)
    await Add_global_task.next()


@dp.message_handler(state=Add_global_task.description)
async def add_decription_global_task(message: types.Message, state: FSMContext):
    await message.delete()
    await state.update_data(description=message.text)
    global owner_message_bot
    owner_message_bot = await owner_message_bot.edit_text('Укажите сроки выполнения задачи в формате "dd/mm/yyyy"')
    owner_message_bot = await owner_message_bot.edit_reply_markup(markup_cancel)
    await Add_global_task.next()


@dp.message_handler(state=Add_global_task.deadline)
async def add_deadline_global_task(message: types.Message, state: FSMContext):
    await message.delete()
    global owner_message_bot
    if re.match(date_pattern, message.text):
        await state.update_data(deadline=message.text)
        await Add_global_task.next()
        await state.update_data(owner_task=message.from_user.id)
        owner_message_bot = await owner_message_bot.edit_text('Задача создана.')
        owner_message_bot = await owner_message_bot.edit_reply_markup(markup_menu)
        data_task = await state.get_data()
        print(data_task)
        add_brigade_task('global', data_task['executor'], data_task['name_task'],
                         data_task['description'], data_task['deadline'], data_task['owner_task'])
        await state.finish()
    else:
        owner_message_bot = await owner_message_bot.edit_text('Введена не верная дата')
        owner_message_bot = await owner_message_bot.edit_reply_markup(markup_cancel)


@dp.message_handler(state=Add_project_task.executor)
async def add_executor_project_task(message: types.Message, state: FSMContext):
    await message.delete()
    global owner_message_bot
    project = select_one_project(message.text)
    if project:
        await state.update_data(executor=message.text)
        owner_message_bot = await owner_message_bot.edit_text('Введите название задачи')
        owner_message_bot = await owner_message_bot.edit_reply_markup(markup_cancel)
        await Add_project_task.next()
    else:
        owner_message_bot = await owner_message_bot.edit_text('Такого проекта нету, повторите ввод заного')
        owner_message_bot = await owner_message_bot.edit_reply_markup(markup_cancel)


@dp.message_handler(state=Add_project_task.name_task)
async def add_name_project_task(message: types.Message, state: FSMContext):
    await message.delete()
    await state.update_data(name_task=message.text)
    global owner_message_bot
    owner_message_bot = await owner_message_bot.edit_text('Введите описание задачи')
    owner_message_bot = await owner_message_bot.edit_reply_markup(markup_cancel)
    await Add_project_task.next()


@dp.message_handler(state=Add_project_task.description)
async def add_decription_project_task(message: types.Message, state: FSMContext):
    await message.delete()
    await state.update_data(description=message.text)
    global owner_message_bot
    owner_message_bot = await owner_message_bot.edit_text('Укажите сроки выполнения задачи в формате "dd/mm/yyyy"')
    owner_message_bot = await owner_message_bot.edit_reply_markup(markup_cancel)
    await Add_project_task.next()


@dp.message_handler(state=Add_project_task.deadline)
async def add_deadline_global_task(message: types.Message, state: FSMContext):
    await message.delete()
    global owner_message_bot
    if re.match(date_pattern, message.text):
        await state.update_data(deadline=message.text)
        await Add_project_task.next()
        await state.update_data(owner_task=message.from_user.id)
        owner_message_bot = await owner_message_bot.edit_text('Задача создана.')
        owner_message_bot = await owner_message_bot.edit_reply_markup(markup_menu)
        data_task = await state.get_data()
        print(data_task)
        add_brigade_task('project', data_task['executor'], data_task['name_task'],
                         data_task['description'], data_task['deadline'], data_task['owner_task'])
        await state.finish()
    else:
        owner_message_bot = await owner_message_bot.edit_text('Введена не верная дата')
        owner_message_bot = await owner_message_bot.edit_reply_markup(markup_cancel)


@dp.message_handler(state=Add_mini_task.executor)
async def add_executor_mini_task(message: types.Message, state: FSMContext):
    await message.delete()
    global owner_message_bot
    users = select_one_user(message.text)
    if users:
        await state.update_data(executor=message.text)
        owner_message_bot = await owner_message_bot.edit_text('Введите название задачи')
        owner_message_bot = await owner_message_bot.edit_reply_markup(markup_cancel)
        await Add_mini_task.next()
    else:
        owner_message_bot = await owner_message_bot.edit_text('Такого сотрудника нету, повторите ввод заного')
        owner_message_bot = await owner_message_bot.edit_reply_markup(markup_cancel)


@dp.message_handler(state=Add_mini_task.name_task)
async def add_name_mini_task(message: types.Message, state: FSMContext):
    await message.delete()
    await state.update_data(name_task=message.text)
    global owner_message_bot
    owner_message_bot = await owner_message_bot.edit_text('Введите время до которого нужно выполнить задачу в формате HH:MM')
    owner_message_bot = await owner_message_bot.edit_reply_markup(markup_cancel)
    await Add_mini_task.next()


@dp.message_handler(state=Add_mini_task.deadline)
async def add_deadline_mini_task(message: types.Message, state: FSMContext):
    await message.delete()
    global owner_message_bot
    if re.match(time_pattern, message.text):
        await state.update_data(deadline=message.text)
        await Add_mini_task.next()
        await state.update_data(owner_task=message.from_user.id)
        owner_message_bot = await owner_message_bot.edit_text('Задача создана.')
        owner_message_bot = await owner_message_bot.edit_reply_markup(markup_menu)
        data_task = await state.get_data()
        print(data_task)
        add_empl_task(data_task['executor'], data_task['name_task'], data_task['deadline'], data_task['owner_task'])
        await state.finish()
    else:
        owner_message_bot = await owner_message_bot.edit_text('Введена не верная дата, повторите ввод')
        owner_message_bot = await owner_message_bot.edit_reply_markup(markup_cancel)


@dp.message_handler(state=Del_task.name_task)
async def delete_task(message: types.Message, state: FSMContext):
    await message.delete()
    global owner_message_bot
    if select_one_task(message.text):
        await state.update_data(name_task=message.text)
        del_task(message.text)
        owner_message_bot = await owner_message_bot.edit_text('Задача удалена')
        owner_message_bot = await owner_message_bot.edit_reply_markup(markup_menu)
        await state.finish()
    else:
        owner_message_bot = await owner_message_bot.edit_text('Такой задачи нету в списке, повторите ввод')
        owner_message_bot = await owner_message_bot.edit_reply_markup(markup_cancel)