from aiogram.utils.keyboard import KeyboardButton, ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup


def end_dialog() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text=r'👋🏻 Закончить диалог')

    keyboard.adjust(2)
    return keyboard.as_markup(resize_keyboard=True)
