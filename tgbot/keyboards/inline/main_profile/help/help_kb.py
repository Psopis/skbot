from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def helps_kb():
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(
        text="📚База знаний",callback_data='Base_of_know'
    )
    )

    kb.row(InlineKeyboardButton(
        text="🔙Вернутся в профиль", callback_data="back_in_profile"
    )
    )
    return kb.as_markup()
