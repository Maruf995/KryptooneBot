from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types 
from aiogram.dispatcher import FSMContext

from filters import IsPrivate
from loader import dp
from utils.db_api import quick_commands as commands
from states import bot_mailing

@dp.message_handler(text='/start')
async def start(message: types.Message):
    await message.answer(f'start')


@dp.message_handler(IsPrivate(), text='/mailing')
async def start_mailing(message: types.Message):
    await message.answer(f'Введите текст рассылки: ')
    await bot_mailing.text.set()



@dp.message_handler(IsPrivate(), state=bot_mailing.text)
async def mailing_text(message: types.Message, state: FSMContext):
    answer  = message.text
    markup = InlineKeyboardMarkup(row_width=2, 
                                        inline_keyboard=[
                                            [
                                                InlineKeyboardButton(text='Добавить Фотографию', callback_data='add_photo'),
                                                InlineKeyboardButton(text='Далее', callback_data='next'),
                                                InlineKeyboardButton(text='Отменить', callback_data='quit')
                                            ]
                                        ])
    await state.update_data(text=answer)
    await message.answer(text=answer, reply_markup=markup)
    await bot_mailing.state.set()

@dp.callback_query_handler(text='text', state=bot_mailing.state)
async def start(call: types.CallbackQuery, state: FSMContext):
    users = await commands.select_all_users()
    data = await state.get_data()
    text = data.get('text')
    for user in users:
        try:
            await dp.bot.send_message(chat_id=user, text=text)
        except Exception:
            pass
    await call.message.answer('Рассылка выполнена.')

@dp.callback_query_handler(text='add_photo', state=bot_mailing.state)
async def add_photo(call: types.CallbackQuery):
    await call.message.answer('Пришлите Фото')
    await bot_mailing.photo.set()

@dp.message_handler(IsPrivate(), state=bot_mailing.photo, content_types=types.ContentType.PHOTO)
async def mailing_text(message: types.Message, state: FSMContext):
    photo_file_id = await message.photo[-1].file_id
    await state.update_data(photo=photo_file_id)
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    markup = InlineKeyboardMarkup(row_width=2,
                                            inline_keyboard=[
                                                [
                                                    InlineKeyboardButton(text='Далее', callback_data='next'),
                                                    InlineKeyboardButton(text='Отменить', callback_data='quit')
                                                    
                                                ]
                                            ])
    await message.answer_photo(photo=photo, caption=text, reply_markup=markup)

@dp.callback_query_handler(text='next', state=bot_mailing.photo)
async def start(call: types.CallbackQuery, state: FSMContext):
    users = await commands.select_all_users()
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    for user in users:
        try:
            await dp.bot.send_photo(chat_id=user, photo=photo, caption=text)
        except Exception:
            pass
    await call.message.answer('Рассылка выполнена.')

@dp.message_handler(IsPrivate(), state=bot_mailing.photo)
async def no_photo(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=2,
                                        inline_keyboard=[
                                            [
                                                InlineKeyboardButton(text='Отменить', callback_data='quit')
                                            ]
                                        ])
    await message.answer('Пришлите мне фотографию', reply_markup=markup)

@dp.callback_query_handler(IsPrivate(), text='quit', state=[bot_mailing.text, bot_mailing.photo, bot_mailing.state])
async def quit(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.message.answer('Рассылка отменена')