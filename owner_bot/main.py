import sys
sys.path.append("D:\\Coding\\Freelance\\telegram_brigade")
import datetime
from time import sleep
import logging
import asyncio
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram import Bot, types
from keyboard import markup_reg, markup_menu, markup_brigade, markup_cancel_alert
from fsm import *
from config import owner_token_bot, data_db
from requests_db import *


bot = Bot(token=owner_token_bot)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

logging.basicConfig(level=logging.INFO)


create_database()
create_users_table()
create_brigade_table()
create_project_table()
create_task_table()


async def deadline_global():
    print('start task global timer')
    while 1:
        list_task = select_global_task()
        if list_task:
            today = datetime.date.today().strftime('%d/%m/%Y').split('/')
            for i in list_task:
                deadline = i[4]
                user_id = i[5]
                status = i[7]
                executor = i[6]
                if int(deadline.split('/')[0])-2 == int(today[0]) and int(status) == 0:
                    await bot.send_message(int(user_id), f'У одной из задач бригады: {executor}\nСрок выполнения подходит к концу', reply_markup=markup_cancel_alert)
                    await asyncio.sleep(18000)
                else:
                    await asyncio.sleep(100)
        await asyncio.sleep(600)


async def deadline_project():
    print('start task project timer')
    while 1:
        list_task = select_project_task()
        if list_task:
            today = datetime.date.today().strftime('%d/%m/%Y').split('/')
            for i in list_task:
                deadline = i[4]
                user_id = i[5]
                status = i[7]
                executor = i[6]
                if int(deadline.split('/')[0])-1 == int(today[0]) and int(status) == 0:
                    await bot.send_message(int(user_id), f'У одной из задач проекта: {executor}\nСрок выполнения подходит к концу', reply_markup=markup_cancel_alert)
                    await asyncio.sleep(18000)
                else:
                    await asyncio.sleep(100)
        await asyncio.sleep(600)


async def deadline_empl():
    print('start task mini timer')
    while 1:
        list_task = select_mini_task()
        if list_task:
            time = datetime.datetime.now().strftime("%H:%M").split(':')
            for i in list_task:
                deadline = i[4]
                user_id = i[5]
                status = i[7]
                executor = i[6]
                if int(deadline.split(':')[0])-2 == int(time[0]) and int(status) == 0:
                    await bot.send_message(int(user_id), f'У сотрудника {executor} срок выполнения одной из задач подходит к концу', reply_markup=markup_cancel_alert)
                    await asyncio.sleep(1200)
                else:
                    await asyncio.sleep(100)
        await asyncio.sleep(300)


if __name__ == '__main__':
    from handlers import dp
    loop = asyncio.get_event_loop()
    loop.create_task(deadline_global())
    loop.create_task(deadline_project())
    loop.create_task(deadline_empl())
    print("Bot pooling")
    executor.start_polling(dp)
