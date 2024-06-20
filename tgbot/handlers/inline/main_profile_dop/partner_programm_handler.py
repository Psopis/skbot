from aiogram import Router, F

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.utils.deep_linking import create_start_link

from infrastructure.database.db_working import UserWorking
from tgbot.keyboards.inline.main_profile.details_kb import profile_dop_section
from tgbot.keyboards.inline.main_profile.partner.partners_kb import partner_dop_section

dop_router = Router()


class states(StatesGroup):
    generation_photo = State()


@dop_router.callback_query(F.data == '_partner_prog')
async def choosing_neuro_to_txtimg(call: CallbackQuery, state: FSMContext):
    await call.answer()
    user = await UserWorking.get_user(call.from_user.id)
    text = f"""В нашем боте включена система промокодов. Приглашайте друзей и зарабатывайте на этом!
Чем больше использований Вашего промокода - тем больше вы будете получать!

Статистика:

Доступно для вывода: {user.referral_balance} ₽
Приведено рефералов: -
"""
    await call.message.edit_text(text=text,
                                 reply_markup=partner_dop_section())


@dop_router.callback_query(F.data == 'back_in_profile')
async def back_button(call: CallbackQuery):
    await call.answer()
    user = await UserWorking.get_user(call.from_user.id)
    start_link = await create_start_link(call.bot, str(call.from_user.id))
    t = f'*Последний день подписки:* {user.date}\n' if user.date else ""
    text = f"""     👤 *Ваш профиль* `{user.username}`\n
*Идентификатор:* `{user.user_id}`\n

📊 Информация:
{t}
*Ваш реферальный баланс:* `{user.referral_balance}`

*Ваша реферальная ссылка:* \n`{start_link}`
                    """
    await call.message.edit_text(text=text, parse_mode="Markdown",
                                 reply_markup=profile_dop_section())
