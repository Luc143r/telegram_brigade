from config import owner_token_bot
from fsm import *
from keyboard import markup_reg, markup_menu, markup_brigade

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


bot = Bot(token=owner_token_bot)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

logging.basicConfig(level=logging.INFO)


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


@dp.callback_query_handler(text='/reg_admin')
async def reg_admin(callback_query: types.CallbackQuery):
    global owner_message_bot
    owner_message_bot = await owner_message_bot.edit_text('Введите свое имя')
    await Registration().role_user.set()
    callback_query.answer()


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


@dp.callback_query_handler(text='/main_menu')
async def send_menu(callback_query: types.CallbackQuery):
    global owner_message_bot
    owner_message_bot = await owner_message_bot.edit_text('Главное меню')
    owner_message_bot = await owner_message_bot.edit_reply_markup(markup_brigade)
    callback_query.answer()


if __name__ == '__main__':
    print('Bot pooling')
    executor.start_polling(dp)
