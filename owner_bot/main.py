import sys
sys.path.append("D:\\Coding\\Freelance\\telegram_brigade")
from requests_db import create_database, create_brigade_table, create_users_table
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


if __name__ == '__main__':
    create_database()
    create_users_table()
    create_brigade_table()
    from handlers import dp
    print("Bot pooling")
    executor.start_polling(dp)
