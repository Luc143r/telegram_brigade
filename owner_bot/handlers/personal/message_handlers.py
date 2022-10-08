from aiogram import types
from main import dp, bot
from fsm import *
from keyboard import *


########################################
# Callback handlers / Обрабочтики кнопок
########################################


@dp.callback_query_handler(text='/reg_admin')
async def reg_admin(callback_query: types.CallbackQuery):
    global owner_message_bot
    owner_message_bot = await owner_message_bot.edit_text('Введите свое имя')
    await Registration().role_user.set()
    callback_query.answer()


@dp.callback_query_handler(text='/main_menu')
async def send_menu(callback_query: types.CallbackQuery):
    global owner_message_bot
    owner_message_bot = await owner_message_bot.edit_text('Главное меню')
    owner_message_bot = await owner_message_bot.edit_reply_markup(markup_brigade)
    callback_query.answer()


@dp.callback_query_handler(text='/add_brigade')
async def add_brigade(callback_query: types.CallbackQuery):
    global owner_message_bot
    owner_message_bot = await owner_message_bot.edit_text('Введите название бригады')
    await Add_brigade().name_brigade.set()
    callback_query.answer()


@dp.callback_query_handler(text='/list_brigade')
async def list_brigade(callback_query: types.CallbackQuery):
    pass


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


@dp.message_handler(state=Registration.role_user)
async def write_firstName(message: types.Message, state: FSMContext):
    await message.delete()
    await state.update_data(role_user='owner')
    await Registration.next()
    await state.update_data(first_name=message.text)
    global owner_message_bot
    owner_message_bot = await owner_message_bot.edit_text('Отлично, а теперь фамилию')
    await Registration.next()


@dp.message_handler(state=Registration.second_name)
async def write_secondName(message: types.Message, state: FSMContext):
    await message.delete()
    await state.update_data(second_name=message.text)
    await Registration.next()
    await state.update_data(tag_telegram=f'@{message.from_user.username}')
    data_user = await state.get_data()
    global owner_message_bot
    print(owner_message_bot)
    owner_message_bot = await owner_message_bot.edit_text('Хорошо. Вы зарегистрировались!')
    await owner_message_bot.edit_reply_markup(markup_menu)
    print(data_user)
    await state.finish()


@dp.message_handler(state=Add_brigade.name_brigade)
async def write_nameBrigade(message: types.Message, state: FSMContext):
    await message.delete()
    await state.update_data(name_brigade=message.text)
    global owner_message_bot
    owner_message_bot = await owner_message_bot.edit_text('Тут будет присылаться список сотрудников, из них нужно будет выбрать ответственного.\nПока что пришли хуйню')
    await Add_brigade.next()


@dp.message_handler(state=Add_brigade.responsible_employer)
async def write_responsibleEmployer(message: types.Message, state: FSMContext):
    await message.delete()
    await state.update_data(responsible_employer=message.text)
    global owner_message_bot
    owner_message_bot = await owner_message_bot.edit_text('Тут тоже будет выбор сотрудников, напиши хуйню пока что')
    await Add_brigade.next()


@dp.message_handler(state=Add_brigade.employers)
async def write_employers(message: types.Message, state: FSMContext):
    await message.delete()
    await state.update_data(employers=message.text)
    global owner_message_bot
    owner_message_bot = await owner_message_bot.edit_text('Красава, все готово, можешь вернуться назад')
    owner_message_bot = await owner_message_bot.edit_reply_markup(markup_menu)
    data_brigade = await state.get_data()
    print(data_brigade)
    await state.finish()
