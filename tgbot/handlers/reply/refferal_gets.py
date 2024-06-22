import os

from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from aiogram import F
from aiogram import Router

from infrastructure.database.db_working import UserWorking
from tgbot.keyboards.inline.generatiob_photo_kb import category_neuro
from tgbot.keyboards.reply.profile_kb import main_user_profile
from openpyxl import load_workbook

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
        wb = load_workbook("stats.xlsx")
        ws = wb.active
        headers = ['user_id', 'Имя', 'referral_id', 'referral_username', 'Баланс', 'Приглашенно пользователей', 'is_subscribe',
                   'Всего было заработано']
        ws.append(headers)
        for user in users:
            referred_by = await user.referred_by
            ws.append([user.user_id, user.username, referred_by.user_id if referred_by else None,
                       referred_by.username if referred_by else None, user.referral_balance,
                       user.users_refered,
                       user.subscribe,
                       user.all_money_reffred])

            # text += f'*Пользователь*:*@{user.username}* \n*Реферальный баланс:* {user.referral_balance} \n*Реферальная ссылка от:*{user_ref}\n*Всего приглашенных пользователей:*{user.users_refered}\n*Всего заработано:*{user.all_money_reffred}🇷🇺RUB\n\n'
        # await message.answer(text=text, reply_markup=main_user_profile(), parse_mode='Markdown')
        wb.save("stats1.xlsx")
        file = FSInputFile('stats1.xlsx')

        await message.answer_document(document=file,
                                      caption="Таблица со статистикой",
                                      reply_markup=main_user_profile())
        os.remove("stats1.xlsx")
