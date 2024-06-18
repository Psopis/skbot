import datetime

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from infrastructure.database.db_working import UserWorking
from tgbot.keyboards.inline.subscrbe_check_kb import subscribe_check
from tgbot.keyboards.reply.profile_kb import main_user_profile

user_router = Router()


@user_router.message(CommandStart())
async def user_start(message: Message):
    await message.answer(
        """Привет! Я - AVRAAM, бот с искусственным интеллектом. \nТы можешь задать мне любой вопрос, а я на него отвечу☺️""",
        reply_markup=main_user_profile())
    print('added', message.from_user.username)
    await UserWorking.add_user(username=message.from_user.username, user_id=message.from_user.id,
                               time=datetime.date.today())
