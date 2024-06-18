from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def profile_subscribes():
    kb = InlineKeyboardBuilder()
    
    kb.row(InlineKeyboardButton(
        text="1 месяц", callback_data="monthSub_1"
    )
    )

    kb.row(InlineKeyboardButton(
        text="3 месяца", callback_data="monthSub_3"
    )
    )
    kb.row(InlineKeyboardButton(
        text="Год", callback_data="monthSub_12"
    )
    )
    kb.row(InlineKeyboardButton(
        text="🔙Вернутся в профиль", callback_data="back_in_profile"
    )
    )
    return kb.as_markup()