import logging
from aiogram import bot, Dispatcher, executor, types
from database import db
from config import bot, dp
from handler import fsmKrypto
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database.db import sql_create

storage = MemoryStorage()

Token = "5440801719:AAGJbB8p5PXTr4iOj063pGwcz7f5bbkfx20"
bot = Bot(Token)
dp = Dispatcher(bot=bot, storage=storage)
ADMIN = [1121073609, 1684336348]


async def on_startup(_):
    sql_create()


fsmKrypto.register_hanlers_fsmKrypto(dp)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
