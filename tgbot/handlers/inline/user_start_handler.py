import datetime

from aiogram import Router
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message

from infrastructure.database.db_working import UserWorking
from tgbot.config import TgBot, load_config
from tgbot.keyboards.inline.subscrbe_check_kb import subscribe_check
from tgbot.keyboards.reply.profile_kb import main_user_profile

user_router = Router()

config = load_config(".env")


@user_router.message(CommandStart())
async def user_start(message: Message, command: CommandObject = None):
    referral = command.args if command else None
    if message.from_user.id in config.tg_bot.admin_ids:
        await UserWorking.add_user(username=message.from_user.username, user_id=message.from_user.id,
                                   employee=True, referred_by=referral)
        await message.answer(text=f"Приветсвую вас Админ {message.from_user.username}",
                             reply_markup=main_user_profile())
    else:
        await message.answer(
            """Привет! Я - AVRAAM, бот с искусственным интеллектом. \nТы можешь задать мне любой вопрос, а я на него отвечу☺️""",
            reply_markup=main_user_profile())
        print('added', message.from_user.username)

        await UserWorking.add_user(username=message.from_user.username, user_id=message.from_user.id,
                                   referred_by=referral)
        if referral:
            await UserWorking.set_referred(user_id=message.from_user.id)

            await UserWorking.plus_one_refferes_user(referral)
