from aiogram import Dispatcher, Bot, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

storage = MemoryStorage()

from utils.db_api.db_gino import db

import data.config as config

loop = asyncio.new_event_loop()
bot = Bot(token=config.BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, loop=loop, storage=MemoryStorage())

__all__ = ['bot', 'storage', 'dp', 'db']