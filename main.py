import logging
from aiogram import bot, Dispatcher, executor, types
from database import db
import database
from config import bot, dp
from handler import fsmKrypto


async def on_startup(_):
    print("Бот запушен!")


fsmKrypto.register_hanlers_fsmKrypto(dp)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.chat.type == 'private':
        pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
