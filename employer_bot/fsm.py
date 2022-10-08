from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext


class Registration(StatesGroup):
    role_user = State()
    first_name = State()
    second_name = State()
    tag_telegram = State()


class Add_brigade(StatesGroup):
    name_brigade = State()
    responsible_employer = State()
    employers = State()


class Create_project(StatesGroup):
    name_project = State()
    responsible_employer = State()
    employers = State()


class Global_task(StatesGroup):
    name_task = State()
    description_task = State()
    deadline_task = State()
    creator_task = State()


class Mini_task(StatesGroup):
    name_task = State()
    deadline_task = State()
    employer_task = State()
    creator_task = State()