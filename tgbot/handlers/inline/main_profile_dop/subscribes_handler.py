from aiogram import Router, F

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.utils.deep_linking import create_start_link

from infrastructure.database.db_working import UserWorking
from infrastructure.yokassa import create_payment, check_payment
from tgbot.keyboards.inline.main_profile.details_kb import profile_dop_section
from tgbot.keyboards.inline.main_profile.subscribes.subscribes_kb import profile_subscribes
from tgbot.keyboards.inline.subscrbe_check_kb import money_set
from tgbot.keyboards.reply.profile_kb import main_user_profile
from tgbot.keyboards.reply.promo_cancel import cancel_subscribes

dop_router = Router()


async def referral_money_set(user_id, balance):
    user = await UserWorking.get_user(user_id)

    if user.referred_by:
        await UserWorking.set_referred(user_id=user_id)
        await UserWorking.set_referral_balance(user.referred_by_id, balance=balance * 0.1)



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
        payment = create_payment(150)
        await call.message.delete()
        await call.message.answer(text='''*Тариф:* на 1 месяц
*Стоимость:* 150 🇷🇺RUB
*Срок действия:* 30 дней
        
*Вы получите доступ к следующим ресурсам:*
- GPT чат-бот
- Генерация изображений
        ''',
                                  reply_markup=money_set(payment), parse_mode='Markdown')

    elif data == '3':
        payment = create_payment(400)
        await call.message.delete()
        await call.message.answer(text='''*Тариф:* на 3 месяца
*Стоимость:* 400 🇷🇺RUB
*Срок действия:* 90 дней
        
*Вы получите доступ к следующим ресурсам:*
- GPT чат-бот
- Генерация изображений
        ''',
                                  reply_markup=money_set(payment), parse_mode='Markdown')

    elif data == '12':
        payment = create_payment(1000)

        await call.message.delete()
        await call.message.answer(text='''*Тариф:* на 1 год
*Стоимость:* 1000 🇷🇺RUB
*Срок действия:* 365 дней

*Вы получите доступ к следующим ресурсам:*
- GPT чат-бот
- Генерация изображений
        ''',
                                  reply_markup=money_set(payment), parse_mode='Markdown')


@dop_router.callback_query(F.data.contains('check_payment'))
async def check_paymentss__(call: CallbackQuery, state: FSMContext):
    payment_id = call.data.split('_')[2]
    value = float(call.data.split('_')[3])
    result = check_payment(payment_id=payment_id)

    print(result)
    if not result:
        await call.answer(text='Оплата не прошла')
    else:
        await referral_money_set(user_id=call.from_user.id, balance=value)

        days = 0
        match int(value):
            case 150:
                days = 30
            case 400:
                days = 90
            case 1000:
                days = 365

        await UserWorking.set_subscribe_true(call.from_user.id, days)
        await call.message.edit_text('Оплата прошла успешно')


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
