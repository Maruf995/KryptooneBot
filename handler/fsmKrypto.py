from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import bot, ADMIN


class fsmAdminKrypto(StatesGroup):
    photo = State()
    description = State()


async def fsm_start(message: types.Message):
    if message.from_user.id in ADMIN:
        await fsmAdminKrypto.photo.set()
        await message.answer("Отправьте фото рекламы")
    else:
        await message.answer("Вы не являетесь владельцем бота!")


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await fsmAdminKrypto.next()
    await message.answer("Описание рекламы:")


async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
        await bot.send_photo(message.from_user.id, data['photo'],
                             caption=f"Description: {data['description']}\n")

        await state.finish()





def register_hanlers_fsmKrypto(dp: Dispatcher):
    dp.register_message_handler(fsm_start, commands=['start'])
    dp.register_message_handler(load_photo, state=fsmAdminKrypto.photo,
                                content_types=['photo'])
    dp.register_message_handler(load_description, state=fsmAdminKrypto.description)
