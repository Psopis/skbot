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


def money_set(cost):
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="Оплатить",
        url='https://example.com'
    )
    )
    kb.row(InlineKeyboardButton(
        text=f"✅Я оплатил {cost}", callback_data=f"check_payment_{cost}"
    )
    )
    kb.row(InlineKeyboardButton(
        text=f"❌Отменить оплату", callback_data="cancel_payment"
    )
    )

    return kb.as_markup()
