from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def category_neuro_generation_photo():
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="SD",
        callback_data="SD_neuro"
    )
    )
    kb.add(InlineKeyboardButton(
        text="Midjourney",
        callback_data="MJ_neuro"
    )
    )
    kb.add(InlineKeyboardButton(
        text="Dalle",
        callback_data="D_neuro"
    )
    )
    kb.row(InlineKeyboardButton(
        text="🔙", callback_data="back_neuro"
    )
    )

    return kb.as_markup()


def category_neuro_remake_photo():
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="ЧТО ТО",
        callback_data="SD_neuro"
    )
    )
    kb.row(InlineKeyboardButton(
        text="🔙", callback_data="back_neuro"
    )
    )

    return kb.as_markup()


def category_neuro_video():
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="Генерация видео",
        callback_data="kand_neuro"
    )
    )
    kb.add(InlineKeyboardButton(
        text="Фото в видео",
        callback_data="img_to_neuro"
    )
    )
    kb.row(InlineKeyboardButton(
        text="🔙", callback_data="back_neuro"
    )
    )

    return kb.as_markup()
