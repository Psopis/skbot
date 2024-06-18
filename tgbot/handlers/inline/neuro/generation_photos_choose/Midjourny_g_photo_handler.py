import datetime
import shutil
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, InputFile, FSInputFile

from infrastructure.database.db_working import UserWorking
from infrastructure.neuro.midjourney.get_img_midjourney import get_midjourney
from infrastructure.neuro.stable_diffusion.get_remade_img import get_SD_picture
from tgbot.keyboards.inline.generatiob_photo_kb import category_neuro
from tgbot.keyboards.inline.neuro_choose_kb import category_neuro_generation_photo
from tgbot.keyboards.reply.profile_kb import main_user_profile

gen_router = Router()


class states(StatesGroup):
    generation_photo = State()


@gen_router.callback_query(F.data == 'MJ_neuro')
async def send_textimg(call: CallbackQuery, state: FSMContext):
    await call.answer()

    await call.message.answer(text='Напишите описание изображения:', reply_markup=None)
    await state.set_state(states.generation_photo)


@gen_router.message(states.generation_photo)
async def send_text_to_img_neuro(message: Message, state: FSMContext):
    msg = await message.answer(text='Навожу магию, секунду 🪄')
    photo = get_midjourney(message.text)
    await msg.delete()
    await message.bot.send_photo(chat_id=message.chat.id, photo=FSInputFile(photo))
    await message.answer(text="Фотография получена!", reply_markup=main_user_profile())
    shutil.rmtree(photo[:-11])
    await state.clear()


@gen_router.callback_query(F.data == 'back_neuro')
async def back_button(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(text='Выберите нейросеть для генерации:',
                                 reply_markup=category_neuro())
