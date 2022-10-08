from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


button_administrator = InlineKeyboardButton(
    'Зарегистрироваться', callback_data='/reg_admin')
markup_reg = InlineKeyboardMarkup()
markup_reg.row(button_administrator)


button_menu = InlineKeyboardButton('Меню', callback_data='/main_menu')
markup_menu = InlineKeyboardMarkup()
markup_menu.row(button_menu)


button_add_brigade = InlineKeyboardButton(
    'Добавить бригаду', callback_data='/add_brigade')
button_check_brigade = InlineKeyboardButton(
    'Мои бригады', callback_data='/list_brigade')
markup_brigade = InlineKeyboardMarkup()
markup_brigade.row(button_add_brigade, button_check_brigade)
