import logging


async def on_startup(dp):
    from loader import  db
    from utils.db_api.db_gino import on_startup
    logging.info('Connecting to PostgreSQL')
    await on_startup(dp)

    # print('Удаление базы')
    # await db.gino.drop_all()

    print('Создание базы')
    await db.gino.create_all()

    print('Бот запущен')


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
