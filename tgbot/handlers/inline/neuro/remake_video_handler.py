import os
import uuid

from aiogram import Router, F
from aiogram.fsm.context import FSMContext

from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message, FSInputFile

from infrastructure.database.db_working import UserWorking
from infrastructure.neuro.img_tovideo_neuro import img_to_vid_generate
from infrastructure.neuro.kandinsky_api import generate
from tgbot.keyboards.inline.neuro_choose_kb import category_neuro_video
from tgbot.keyboards.reply.profile_kb import main_user_profile

gen_router = Router()


class states(StatesGroup):
    generation_video = State()
    img_toVideo = State()


@gen_router.callback_query(F.data == 'video_remake')
async def subscribe_ch(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(text='Выберите нейросеть для генерации:',
                                 reply_markup=category_neuro_video())


@gen_router.callback_query(F.data == 'kand_neuro')
async def send_textimg(call: CallbackQuery, state: FSMContext):
    await call.answer()
    user = await UserWorking.get_user(call.from_user.id)
    if user.subscribe:
        await call.message.delete()
        await call.message.answer(text='Напишите описание видео:', reply_markup=None)
        await state.set_state(states.generation_video)
    else:
        await call.message.delete()
        await call.message.answer(text='Вы не приобрели подписку!', reply_markup=main_user_profile())


@gen_router.message(states.generation_video)
async def send_text_to_img_neuro(message: Message, state: FSMContext):
    msg = await message.answer(text='Навожу магию, секунду 🪄')
    video = await generate(message.text)
    await msg.delete()
    await message.bot.send_video(chat_id=message.chat.id, video=FSInputFile(video))
    await message.answer(text="Видео получено!", reply_markup=main_user_profile())
    os.remove(video)
    await state.clear()


@gen_router.callback_query(F.data == 'img_to_neuro')
async def send_img_to_video(call: CallbackQuery, state: FSMContext):
    await call.answer()
    user = await UserWorking.get_user(call.from_user.id)
    if user.subscribe:
        await call.message.delete()
        await call.message.answer(text='Отправьте изображение для создания видео:', reply_markup=None)
        await state.set_state(states.img_toVideo)
    else:
        await call.message.delete()
        await call.message.answer(text='Вы не приобрели подписку!', reply_markup=main_user_profile())


@gen_router.message(states.img_toVideo)
async def send_text_to_img_neuro(message: Message, state: FSMContext):
    msg = await message.answer(text='Навожу магию, секунду 🪄')
    photo = uuid.uuid1()
    await message.bot.download(file=message.photo[-1].file_id,
                               destination=f'infrastructure/neuro/down_video/{photo}.jpg')

    video = img_to_vid_generate(f'infrastructure/neuro/down_video/{photo}.jpg')
    os.remove(f'infrastructure/neuro/down_video/{photo}.jpg')
    await msg.delete()
    await message.bot.send_video(chat_id=message.chat.id, video=FSInputFile(video))
    await message.answer(text="Видео получено!", reply_markup=main_user_profile())

    os.remove(video)
    await state.clear()


@gen_router.callback_query(F.data == 'back_neuro')
async def back_button(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(text='Выберите нейросеть для генерации:',
                                 reply_markup=category_neuro_video())
