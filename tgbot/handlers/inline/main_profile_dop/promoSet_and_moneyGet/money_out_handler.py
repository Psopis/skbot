from aiogram import Router, F

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from infrastructure.database.db_working import UserWorking
from tgbot.keyboards.inline.main_profile.partner.partners_kb import partner_dop_section
from tgbot.keyboards.reply.profile_kb import main_user_profile
from tgbot.keyboards.reply.promo_cancel import cancel_promo

dop_router = Router()


class states(StatesGroup):
    money_set = State()


@dop_router.callback_query(F.data == 'get_money')
async def textfor_set_promorcode(call: CallbackQuery, state: FSMContext):
    await call.answer()

    text = f"""Введите номер телефона или банковской карты с указанием банка для перевода.

Если у вас подключено СБП, то укажите телефон и банк на который нужно перевести деньги.

Пример: 79999999999 Тинькофф  или 49993888277716666 
Альфа Банк"""
    await call.message.answer(text=text,
                              reply_markup=cancel_promo())
    # await state.set_state(states.money_set)


# @dop_router.message(states.money_set)
# async def set_promocode(message: Message, state: FSMContext):
#     await UserWorking.set_your_promo(message.from_user.id, message.text)
#     await message.answer(text=f'Промокод {message.text} создан!')
#     await state.clear()

@dop_router.message(F.text == '❌Отменть')
async def set_promocode(message: Message, state: FSMContext):
    await message.answer(text=f'Действие отменено', reply_markup=main_user_profile())
    user = await UserWorking.get_user(message.from_user.id)
    text = f"""В нашем боте включена система промокодов. Приглашайте друзей и зарабатывайте на этом!
Чем больше использований Вашего промокода - тем больше вы будете получать!

Статистика:



Доступно для вывода: 0 ₽
Приведено рефералов: 0
Награда за активацию: -"""
    await message.answer(text=text, parse_mode="Markdown",
                         reply_markup=partner_dop_section())
    await state.clear()
