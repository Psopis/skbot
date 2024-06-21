from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F
from aiogram import Router

from infrastructure.database.db_working import UserWorking
from tgbot.keyboards.inline.generatiob_photo_kb import category_neuro
from tgbot.keyboards.reply.profile_kb import main_user_profile

router = Router()
router.message.filter(
    F.chat.type == "private"
)


@router.message(Command('r'))
async def refferals_gets_all(message: Message):
    user = await UserWorking.get_user(message.from_user.id)
    text = 'Пользователи с реферальной ссылкой или реферальным балансом\n\n'
    if user.is_employee:
        users = await UserWorking.get_all_users_refereded()

        for user in users:
            if user.referred_by_id is None:
                user_ref = '-'
            else:
                user_ref = (await UserWorking.get_user(user.referred_by_id)).username
            text += f'*Пользователь*:*@{user.username}* \n*Реферальный баланс:* {user.referral_balance} \n*Реферальная ссылка от:*{user_ref}\n*Всего приглашенных пользователей:*{user.users_refered}\n*Всего заработано:*{user.all_money_reffred}🇷🇺RUB\n\n'
        await message.answer(text=text, reply_markup=main_user_profile(), parse_mode='Markdown')
