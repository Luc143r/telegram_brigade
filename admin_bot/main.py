from config import admin_token_bot
from fsm import *

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

import asyncio
import logging
from time import sleep


bot = Bot(token=admin_token_bot)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

logging.basicConfig(level=logging.INFO)

owner_message_bot = 0


@dp.message_handler(commands='start')
async def command_start(message: types.Message):
    button_administrator = InlineKeyboardButton(
        'Зарегистрироваться', callback_data='/reg_admin')
    markup_reg = InlineKeyboardMarkup()
    markup_reg.row(button_administrator, button_employer)
    global owner_message_bot
    owner_message_bot = await bot.send_message(message.chat.id, f'{message.from_user.username}, приветствую. Пройди простую регистрацию', reply_markup=markup_reg)
    await message.delete()


@dp.message_handler(commands='reg')
async def command_reg(message: types.Message):
    button_administrator = InlineKeyboardButton(
        'Руководитель', callback_data='/reg_admin')
    button_employer = InlineKeyboardButton(
        'Сотрудник', callback_data='/reg_employer')
    markup_reg = InlineKeyboardMarkup()
    markup_reg.row(button_administrator, button_employer)
    global owner_message_bot
    owner_message_bot = await bot.send_message(message.chat.id, f'{message.from_user.username}, приветствую. Пройди простую регистрацию в зависимости от твоей роли в организации', reply_markup=markup_reg)
    await message.delete()


@dp.callback_query_handler(text='/reg_admin')
async def reg_admin(callback_query: types.CallbackQuery):
    await owner_message_bot.edit_text('Введите свое имя')
    await Registration().role_user.set()
    callback_query.answer()


@dp.message_handler(state=Registration.role_user)
async def write_firstName(message: types.Message, state: FSMContext):
    await message.delete()
    await state.update_data(first_name=message.text)
    await owner_message_bot.edit_text('Отлично, а теперь фамилию')

    await Registration.next()


@dp.message_handler(state=Registration.second_name)
async def write_secondName(message: types.Message, state: FSMContext):
    await message.delete()
    await state.update_data(second_name=message.text)
    back_button = ReplyKeyboard
    await owner_message_bot.edit_text('Хорошо. Вы зарегистрировались!')
    await Registration.next()
    await state.update_data(tag_telegram=f'@{message.from_user.username}')
    data_user = await state.get_data()
    print(data_user)
    await state.finish()


if __name__ == '__main__':
    print('Bot pooling')
    executor.start_polling(dp)
