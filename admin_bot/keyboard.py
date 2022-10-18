from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


#############
# Кнопка меню
#############


button_menu = InlineKeyboardButton('Меню', callback_data='/main_menu')
markup_menu = InlineKeyboardMarkup()
markup_menu.row(button_menu)


###############
# Кнопка отмены
###############


button_cancel = InlineKeyboardButton('Отмена', callback_data='/cancel')
markup_cancel = InlineKeyboardMarkup()
markup_cancel.row(button_cancel)


####################
# Убрать уведомление
####################


button_cancel_alert = InlineKeyboardButton(
    'Убрать уведомление', callback_data='/cancel_alert')
markup_cancel_alert = InlineKeyboardMarkup()
markup_cancel_alert.row(button_cancel_alert)


##############
# Главное меню
##############
######################
# Управление проектами
######################


button_add_project = InlineKeyboardButton(
    'Добавить проект', callback_data='/add_project')
button_check_project = InlineKeyboardButton(
    'Посмотреть проекты', callback_data='/check_project')
button_del_project = InlineKeyboardButton(
    'Удалить проект', callback_data='/del_project')


#####################
# Управление задачами
#####################


button_add_project_task = InlineKeyboardButton(
    'Добавить проектную задачу', callback_data='/add_project_task')
button_add_mini_task = InlineKeyboardButton(
    'Добавить задачу сотруднику', callback_data='/add_mini_task')

button_del_task = InlineKeyboardButton(
    'Удалить задачу', callback_data='/del_task')
button_check_task = InlineKeyboardButton(
    'Посмотреть задачи', callback_data='/check_task')

markup_brigade = InlineKeyboardMarkup()
markup_brigade.row(button_add_project,
                   button_check_project, button_del_project)
markup_brigade.row(button_add_project_task, button_add_mini_task)
markup_brigade.row(button_del_task, button_check_task)
