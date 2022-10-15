from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


####################
# Кнопка регистрации
####################


button_administrator = InlineKeyboardButton(
    'Зарегистрироваться', callback_data='/reg_admin')
markup_reg = InlineKeyboardMarkup()
markup_reg.row(button_administrator)


#############
# Кнопка меню
#############


button_menu = InlineKeyboardButton('Меню', callback_data='/main_menu')
markup_menu = InlineKeyboardMarkup()
markup_menu.row(button_menu)


##############
# Главное меню
##############


button_add_brigade = InlineKeyboardButton(
    'Добавить бригаду', callback_data='/add_brigade')
button_check_brigade = InlineKeyboardButton(
    'Мои бригады', callback_data='/list_brigade')
button_del_brigade = InlineKeyboardButton('Удалить бригаду', callback_data='/del_brigade')

######################
# Управление проектами
######################


button_add_project = InlineKeyboardButton('Добавить проект', callback_data='/add_project')
button_check_project = InlineKeyboardButton('Посмотреть проекты', callback_data='/check_project')
button_del_project = InlineKeyboardButton('Удалить проект', callback_data='/del_project')


#####################
# Управление задачами
#####################


button_add_global_task = InlineKeyboardButton('Добавить глобальную задачу', callback_data='/add_global_task')
button_add_project_task = InlineKeyboardButton('Добавить проектную задачу', callback_data='/add_project_task')
button_add_mini_task = InlineKeyboardButton('Добавить задачу сотруднику', callback_data='/add_mini_task')

button_del_task = InlineKeyboardButton('Удалить задачу', callback_data='/del_task')
button_check_task = InlineKeyboardButton('Посмотреть задачи', callback_data='/check_task')

markup_brigade = InlineKeyboardMarkup()
markup_brigade.row(button_add_brigade, button_check_brigade, button_del_brigade)
markup_brigade.row(button_add_project, button_check_project, button_del_project)
markup_brigade.row(button_add_global_task, button_add_project_task, button_add_mini_task)
markup_brigade.row(button_del_task, button_check_task)

