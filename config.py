from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

Token = "5440801719:AAGJbB8p5PXTr4iOj063pGwcz7f5bbkfx20"
bot = Bot(Token)
dp = Dispatcher(bot=bot, storage=storage)
ADMIN = [1121073609, 1684336348]
