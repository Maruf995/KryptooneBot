from cgitb import handler
from aiogram import Dispatcher, Bot, executor, types
import asyncio



from data import config

loop = asyncio.new_event_loop()
bot = Bot(token=config.BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, loop=loop)




async def on_startup(dp):

    print('Бот запущен')

if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, on_startup=on_startup)

