from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext


class Registration(StatesGroup):
    role_user = State()
    name = State()
    tag_telegram = State()


class Add_brigade(StatesGroup):
    name_brigade = State()
    responsible_employer = State()
    employers = State()
