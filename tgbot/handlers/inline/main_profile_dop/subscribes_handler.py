from aiogram import Router, F

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.utils.deep_linking import create_start_link

from infrastructure.database.db_working import UserWorking
from tgbot.keyboards.inline.main_profile.details_kb import profile_dop_section
from tgbot.keyboards.inline.main_profile.subscribes.subscribes_kb import profile_subscribes
from tgbot.keyboards.inline.subscrbe_check_kb import money_set
from tgbot.keyboards.reply.profile_kb import main_user_profile
from tgbot.keyboards.reply.promo_cancel import cancel_subscribes

dop_router = Router()


async def referral_money_set(reffered_by, balance):
    user = await UserWorking.get_user(reffered_by)
    if user.referred_by:
        await UserWorking.set_referral_balance(reffered_by, balance * 0.1)


class states(StatesGroup):
    generation_photo = State()
    money_set = State()


@dop_router.callback_query(F.data == '_Subscribe')
async def choosing_neuro_to_txtimg(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_text(text='Выберите тарифный план',
                                 reply_markup=profile_subscribes())


@dop_router.callback_query(F.data.contains('monthSub'))
async def choosing_neuro_to_txtimg(call: CallbackQuery, state: FSMContext):
    data = call.data.split('_')[1]
    if data == '1':
        await call.message.delete()
        await call.message.answer(text='Вы выбрали подписку на 1 месяц',
                                  reply_markup=money_set(100))

    elif data == '3':
        await call.message.delete()
        await call.message.answer(text='Вы выбрали подписку на 3 месяца',
                                  reply_markup=money_set(200))

    elif data == '12':
        await call.message.delete()
        await call.message.answer(text='Вы выбрали подписку на год',
                                  reply_markup=money_set(300))


@dop_router.callback_query(F.data.contains('check_payment'))
async def check_paymentss__(call: CallbackQuery, state: FSMContext):
    data = call.data.split('_')[2]
    await referral_money_set(reffered_by=call.from_user.id, balance=int(data))
    await UserWorking.set_subscribe_true(call.from_user.id)
    await call.message.edit_text('Вы оплатили подписку')


@dop_router.callback_query(F.data == 'cancel_payment')
async def cancel_pament___(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text='Выберите тарифный план',
                                 reply_markup=profile_subscribes())


@dop_router.message(F.text == '❌Отменть')
async def set_promocode(message: Message, state: FSMContext):
    await message.answer(text=f'Действие отменено', reply_markup=main_user_profile())

    await message.answer(text='Выберите тарифный план',
                         reply_markup=profile_subscribes())


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
