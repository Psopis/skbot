import datetime
import shutil
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.utils.deep_linking import create_start_link

from infrastructure.database.db_working import UserWorking
from tgbot.keyboards.inline.main_profile.details_kb import profile_dop_section
from tgbot.keyboards.inline.main_profile.help.help_kb import helps_kb
from tgbot.keyboards.inline.main_profile.partner.partners_kb import partner_dop_section
from tgbot.keyboards.inline.main_profile.subscribes.subscribes_kb import profile_subscribes

dop_router = Router()


class states(StatesGroup):
    generation_photo = State()


@dop_router.callback_query(F.data == '_help')
async def choosing_neuro_to_txtimg(call: CallbackQuery, state: FSMContext):
    await call.answer()

    text = f"""Перед обращением в поддержку - загляните в нашу базу знаний.
Возможно,там уже имеется ответ на ваш вопрос.

Если Вы не нашли ответ на свой вопрос, напишите нам. 
Мы всегда будем рады помочь ❤️"""
    await call.message.edit_text(text=text,
                                 reply_markup=helps_kb())


@dop_router.callback_query(F.data == 'Base_of_know')
async def choosing_neuro_to_txtimg(call: CallbackQuery, state: FSMContext):
    await call.answer()

    text = f"""ШАГ ПЕРВЫЙ
👶 Составляем простой запрос
Для генерации картинки на самом деле достаточно и одного-двух слов. И такие результаты тоже получаются качественными. Но если вы введете пару слов без дополнительных параметров, то остальные детали нейросеть хаотично «додумает» сама. Поэтому лучше использовать базовые знания, чтобы затем развить запрос в более комплексный.

Многие нейросети переходят к тому, чтобы понимать естественный язык, — такой, на котором люди общаются друг с другом. Пробуйте описывать объекты и сцены, как вы рассказывали бы про будущую картинку своему приятелю.

Составляйте запросы на английском языке
Нейросети обучались на парах картинка-описание на английском языке, поэтому лучше всего воспринимают запросы на «родном» языке. Они могут воспринимать другие языки и даже понимать эмодзи, но результаты будут непредсказуемы. Если не знаете английский, пользуйтесь нейросетевым переводчиком DeepL — он понимает контекст лучше, чем Google Translate.

Объект. Основа практически любого запроса — именно он будет в центре всего рисунка. Очевидно, что в первую очередь надо придумать именно его. Например, кот, волшебник, священник, ангел, император, некромант, рок-звезда, город, королева, дом, храм, ферма, машина, пейзаж, гора, река.

Нейросети обучают на огромной базе изображений из сети. Картинок такого типа в интернете много, поэтому нейросети легко их сгенерируют. Правда, если вписывать в команду исключительно один объект, то результаты вряд ли порадуют разнообразием. Поэтому попробуйте, например, совместить два объекта и получить необычный концепт: кот-геймер, некромант-капиталист, киберпанк-монах.
ШАГ ВТОРОЙ
🦾 Добавляем детали
Уделите время конкретике: придумайте, как расположены объекты на картинке. Напишите не просто «волшебник», а «грустный волшебник в колпаке работает за компьютером в офисе поздно вечером». Не забывайте, что у запросов есть ограничение на количество символов. 

Вот какие базовые детали можно добавить к запросу.

Действия. Сформулируйте действие так, чтобы его можно было наглядно отразить на картинке. Глаголы «стоит» или «идет» помогают гораздо больше, чем «мечтает» или «беспокоится». Если вам все же нужно изображение с неочевидным действием, то добавьте детали: не просто «размышляет», а «сидит, погруженный в мысли»."""
    await call.message.edit_text(text=text,
                                 reply_markup=profile_dop_section())


@dop_router.callback_query(F.data == 'back_in_profile')
async def back_button(call: CallbackQuery):
    await call.answer()
    user = await UserWorking.get_user(call.from_user.id)
    start_link = await create_start_link(call.bot, str(call.from_user.id))
    t = f'*Последний день подписки:* {user.date}\n' if user.date else ""
    text = f"""     👤 *Ваш профиль* `{user.username}`\n
*Идентификатор:* `{user.user_id}`\n

📊 Инф1ормация:
{t}
*Ваш реферальный баланс:* `{user.referral_balance}`

*Ваша реферальная ссылка:* \n`{start_link}`
                    """
    await call.message.edit_text(text=text, parse_mode="Markdown",
                                 reply_markup=profile_dop_section())
