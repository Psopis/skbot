from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def subscribe_check():
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="⛓️Подписаться",
        url='https://t.me/qwdasdwasd'
    )
    )
    kb.row(InlineKeyboardButton(
        text="✅Я подписался", callback_data="subscribe_check_"
    )
    )

    return kb.as_markup()
