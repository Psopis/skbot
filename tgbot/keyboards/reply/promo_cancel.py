from aiogram.utils.keyboard import KeyboardButton, ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup


def cancel_promo() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text=r'❌Отменть')

    keyboard.adjust(2)
    return keyboard.as_markup(resize_keyboard=True)


def cancel_subscribes() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text=r'❌Отменть')

    keyboard.adjust(2)
    return keyboard.as_markup(resize_keyboard=True)
