from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext


class Registration(StatesGroup):
    role_user = State()
    name = State()
    tag_telegram = State()


class Add_brigade(StatesGroup):
    name_brigade = State()
    responsible_employer = State()

class Del_brigade(StatesGroup):
    name_brigade = State()


class Add_project(StatesGroup):
    brigade = State()
    name_project = State()
    employers = State()


class Del_project(StatesGroup):
    name_project = State()


class Add_global_task(StatesGroup):
    executor = State()
    name_task = State()
    description = State()
    deadline = State()
    owner_task = State()


class Add_project_task(StatesGroup):
    executor = State()
    name_task = State()
    description = State()
    deadline = State()
    owner_task = State()


class Add_mini_task(StatesGroup):
    executor = State()
    name_task = State()
    deadline = State()
    owner_task = State()
