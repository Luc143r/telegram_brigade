from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext


class Registration(StatesGroup):
    role_user = State()
    name = State()
    tag_telegram = State()


class Done_task(StatesGroup):
    name_task = State()
