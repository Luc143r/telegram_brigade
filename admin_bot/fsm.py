from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext


class Add_project(StatesGroup):
    brigade = State()
    name_project = State()
    employers = State()


class Del_project(StatesGroup):
    name_project = State()


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


class Del_task(StatesGroup):
    name_task = State()


class Done_task(StatesGroup):
    name_task = State()
