from aiogram.types import Message
from aiogram import F
from aiogram import Router
from aiogram.utils.deep_linking import create_start_link

from infrastructure.database.db_working import UserWorking
from tgbot.keyboards.inline.main_profile.details_kb import profile_dop_section

router = Router()
router.message.filter(
    F.chat.type == "private"
)


@router.message(F.text == "🏡Профиль")
async def main_profile_text(message: Message):
    print(message.from_user.id)
    user = await UserWorking.get_user(message.from_user.id)
    start_link = await create_start_link(message.bot, str(message.from_user.id))
    t = f'*Последний день подписки:* {user.date}\n' if user.date else ""
    text = f"""     👤 *Ваш профиль* `{user.username}`\n
*Идентификатор:* `{user.user_id}`\n

📊 Информация:
{t}
*Ваш реферальный баланс:* `{user.referral_balance}`

*Ваша реферальная ссылка:* \n`{start_link}`
                    """
    await message.answer(text=text, parse_mode="Markdown", reply_markup=profile_dop_section())
