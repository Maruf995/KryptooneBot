import logging
from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from filters import IsPrivate
from loader import dp
from utils.db_api import quick_commands as commands
from states import bot_mailing

from data.config import ADMIN





@dp.message_handler(IsPrivate(), text='/mailing', chat_id=ADMIN)
async def start_mailing(message: types.Message):
    await message.answer(f'Введите текст рассылки:')
    await bot_mailing.text.set()


@dp.message_handler(IsPrivate(), state=bot_mailing.text, chat_id=ADMIN)
async def mailing_text(message: types.Message, state: FSMContext):
    answer = message.text
    markup = InlineKeyboardMarkup(row_width=6,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text='фотографию', callback_data='add_photo'),
                                          InlineKeyboardButton(text='Файл', callback_data='add_document'),
                                          InlineKeyboardButton(text='Видео', callback_data='add_video'),

                                      ],
                                      [
                                          InlineKeyboardButton(text='Голосовое Сообщение', callback_data='add_voice'),
                                          InlineKeyboardButton(text='Аудио', callback_data='add_audio'),
                                          InlineKeyboardButton(text='Отменить', callback_data='quit'),
                                      ],
                                      [
                                          InlineKeyboardButton(text='Далее', callback_data='next'),
                                      ]
                                  ])
    await state.update_data(text=answer)
    await message.answer(text=answer, reply_markup=markup)
    await bot_mailing.state.set()


@dp.callback_query_handler(text='next', state=bot_mailing.state, chat_id=ADMIN)
async def start(call: types.CallbackQuery, state: FSMContext):
    users = await commands.select_all_users()
    data = await state.get_data()
    text = data.get('text')
    await state.finish()
    for user in users:
        try:
            await dp.bot.send_message(chat_id=user.user_id, text=text)
            await sleep(0.33)
        except Exception as err:
            logging.exception(err)
            pass
    await call.message.answer('Рассылка выполнена.')


@dp.callback_query_handler(text='add_document', state=bot_mailing.state, chat_id=ADMIN)
async def add_document(call: types.CallbackQuery):
    await call.message.answer('Пришлите Файл')
    await bot_mailing.document.set()


@dp.callback_query_handler(text='add_audio', state=bot_mailing.state, chat_id=ADMIN)
async def add_audio(call: types.CallbackQuery):
    await call.message.answer('Пришлите Аудио')
    await bot_mailing.audio.set()


@dp.callback_query_handler(text='add_photo', state=bot_mailing.state, chat_id=ADMIN)
async def add_photo(call: types.CallbackQuery):
    await call.message.answer('Пришлите фото')
    await bot_mailing.photo.set()


@dp.callback_query_handler(text='add_video', state=bot_mailing.state, chat_id=ADMIN)
async def add_video(call: types.CallbackQuery):
    await call.message.answer('Пришлите видео')
    await bot_mailing.video.set()


@dp.callback_query_handler(text='add_voice', state=bot_mailing.state, chat_id=ADMIN)
async def add_voice(call: types.CallbackQuery):
    await call.message.answer('Пришлите Голосовое Сообщение')
    await bot_mailing.voice.set()


@dp.message_handler(IsPrivate(), state=bot_mailing.photo, content_types=types.ContentType.PHOTO, chat_id=ADMIN)
async def mailing_text(message: types.Message, state: FSMContext):
    photo_file_id = message.photo[-1].file_id  # Возвращает file_id фотографии с наилучшим разрешением
    await state.update_data(photo=photo_file_id)
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    markup = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text='Отправить Рассылку', callback_data='next'),
                                          InlineKeyboardButton(text='Отменить', callback_data='quit')
                                      ]
                                  ])
    await message.answer_photo(photo=photo, caption=text, reply_markup=markup)


@dp.message_handler(IsPrivate(), state=bot_mailing.document, content_types=types.ContentType.DOCUMENT, chat_id=ADMIN)
async def mailing_text(message: types.Message, state: FSMContext):
    document_file_id = message.document.file_id
    await state.update_data(document=document_file_id)
    data = await state.get_data()
    text = data.get('text')
    document = data.get('document')
    markup = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text='Отправить Рассылку', callback_data='next'),
                                          InlineKeyboardButton(text='Отменить', callback_data='quit')
                                      ]
                                  ])
    await message.answer_document(document=document, caption=text, reply_markup=markup)


@dp.message_handler(IsPrivate(), state=bot_mailing.audio, content_types=types.ContentType.AUDIO, chat_id=ADMIN)
async def mailing_text(message: types.Message, state: FSMContext):
    audio_file_id = message.audio.file_id
    await state.update_data(audio=audio_file_id)
    data = await state.get_data()
    text = data.get('text')
    audio = data.get('audio')
    markup = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text='Отправить Рассылку', callback_data='next'),
                                          InlineKeyboardButton(text='Отменить', callback_data='quit')
                                      ]
                                  ])
    await message.answer_audio(audio=audio, caption=text, reply_markup=markup)


@dp.message_handler(IsPrivate(), state=bot_mailing.voice, content_types=types.ContentType.VOICE, chat_id=ADMIN)
async def mailing_text(message: types.Message, state: FSMContext):
    voice_file_id = message.voice.file_id
    await state.update_data(voice=voice_file_id)
    data = await state.get_data()
    text = data.get('text')
    voice = data.get('voice')
    markup = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text='Отправить Рассылку', callback_data='next'),
                                          InlineKeyboardButton(text='Отменить', callback_data='quit')
                                      ]
                                  ])
    await message.answer_voice(voice=voice, caption=text, reply_markup=markup)


@dp.message_handler(IsPrivate(), state=bot_mailing.video, content_types=types.ContentType.VIDEO, chat_id=ADMIN)
async def mailing_text(message: types.Message, state: FSMContext):
    video_file_id = message.video.file_id
    await state.update_data(video=video_file_id)
    data = await state.get_data()
    text = data.get('text')
    video = data.get('video')
    markup = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text='Отправить Рассылку', callback_data='next'),
                                          InlineKeyboardButton(text='Отменить', callback_data='quit')
                                      ]
                                  ])
    await message.answer_video(video=video, caption=text, reply_markup=markup)


@dp.callback_query_handler(text='next', state=bot_mailing.document, chat_id=ADMIN)
async def start(call: types.CallbackQuery, state: FSMContext):
    users = await commands.select_all_users()
    data = await state.get_data()
    text = data.get('text')
    document = data.get('document')
    await state.finish()
    for user in users:
        try:
            await dp.bot.send_document(chat_id=user.user_id, document=document, caption=text)
            await sleep(0.33)
        except Exception as err:
            logging.exception(err)
            pass
    await call.message.answer('Рассылка выполнена.')


@dp.callback_query_handler(text='next', state=bot_mailing.video, chat_id=ADMIN)
async def start(call: types.CallbackQuery, state: FSMContext):
    users = await commands.select_all_users()
    data = await state.get_data()
    text = data.get('text')
    video = data.get('video')
    await state.finish()
    for user in users:
        try:
            await dp.bot.send_video(chat_id=user.user_id, video=video, caption=text)
            await sleep(0.33)
        except Exception as err:
            logging.exception(err)
            pass
    await call.message.answer('Рассылка выполнена.')


@dp.callback_query_handler(text='next', state=bot_mailing.audio, chat_id=ADMIN)
async def start(call: types.CallbackQuery, state: FSMContext):
    users = await commands.select_all_users()
    data = await state.get_data()
    text = data.get('text')
    audio = data.get('audio')
    await state.finish()
    for user in users:
        try:
            await dp.bot.send_audio(chat_id=user.user_id, audio=audio, caption=text)
            await sleep(0.33)
        except Exception as err:
            logging.exception(err)
            pass
    await call.message.answer('Рассылка выполнена.')


@dp.callback_query_handler(text='next', state=bot_mailing.voice, chat_id=ADMIN)
async def start(call: types.CallbackQuery, state: FSMContext):
    users = await commands.select_all_users()
    data = await state.get_data()
    text = data.get('text')
    voice = data.get('voice')
    await state.finish()
    for user in users:
        try:
            await dp.bot.send_voice(chat_id=user.user_id, voice=voice, caption=text)
            await sleep(0.33)
        except Exception as err:
            logging.exception(err)
            pass
    await call.message.answer('Рассылка выполнена.')


@dp.callback_query_handler(text='next', state=bot_mailing.photo, chat_id=ADMIN)
async def start(call: types.CallbackQuery, state: FSMContext):
    users = await commands.select_all_users()
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    await state.finish()
    for user in users:
        try:
            await dp.bot.send_photo(chat_id=user.user_id, photo=photo, caption=text)
            await sleep(0.33)
        except Exception as err:
            logging.exception(err)
            pass
    await call.message.answer('Рассылка выполнена.')


@dp.message_handler(IsPrivate(), state=bot_mailing.photo, chat_id=ADMIN)
async def no_photo(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text='Отменить', callback_data='quit')
                                      ]
                                  ])
    await message.answer('Пришли мне фотографию', reply_markup=markup)


@dp.message_handler(IsPrivate(), state=bot_mailing.document, chat_id=ADMIN)
async def no_document(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text='Отменить', callback_data='quit')
                                      ]
                                  ])
    await message.answer('Пришли мне Документ', reply_markup=markup)


@dp.message_handler(IsPrivate(), state=bot_mailing.audio, chat_id=ADMIN)
async def no_audio(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text='Отменить', callback_data='quit')
                                      ]
                                  ])
    await message.answer('Пришли мне Аудио', reply_markup=markup)


@dp.message_handler(IsPrivate(), state=bot_mailing.video, chat_id=ADMIN)
async def no_video(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text='Отменить', callback_data='quit')
                                      ]
                                  ])
    await message.answer('Пришли мне Видео', reply_markup=markup)


@dp.message_handler(IsPrivate(), state=bot_mailing.voice, chat_id=ADMIN)
async def no_voice(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text='Отменить', callback_data='quit')
                                      ]
                                  ])
    await message.answer('Пришли мне Голосовое Сообщение', reply_markup=markup)


@dp.callback_query_handler(text='quit',
                           state=[bot_mailing.text, bot_mailing.photo, bot_mailing.document, bot_mailing.video,
                                  bot_mailing.voice, bot_mailing.audio, bot_mailing.state],
                           chat_id=ADMIN)
async def quit(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer('Рассылка отменена')
