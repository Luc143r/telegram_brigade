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


#####################
# Управление задачами
#####################


button_check_task = InlineKeyboardButton(
    'Посмотреть задачи', callback_data='/check_task')

markup_brigade = InlineKeyboardMarkup()
markup_brigade.row(button_check_task)
