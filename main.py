from aiogram import bot, executor
import logging
from config import bot, dp
from handler import fsmKrypto


async def on_startup(_):
    print("Бот запушен!")


fsmKrypto.register_hanlers_fsmKrypto(dp)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
