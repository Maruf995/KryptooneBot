from utils.db_api import quick_commands as commands
from utils.db_api.db_gino import db
from data import config
import asyncio


async def db_test():
    await db.set_bind(config.POSTGRES_URI)
    # await db.gino.drop_all()
    # await db.gino.create_all()
    #
    # await commands.add_user(132324, 'Maruf', 'adsd')
    # await commands.add_user(123312, 'asdads', 'sdf')
    # await commands.add_user(1313, 'fs', 'sf')
    # await commands.add_user(1313242543, 'fs', 'fgh')
    # await commands.add_user(13198903, 'fs', 'kj')
    # await commands.add_user(135679013, 'fs', 'ghj')

    users = await commands.select_all_users()
    print(users)

    count = await commands.count_users()
    print(count)

    user = await commands.select_user(1)
    print(user)

    await commands.update_user_name(1, 'New Maruf')

    user = await commands.select_user(1)
    print(user)


# loop = asyncio.get_event_loop()
# loop.run_until_complete(db_test())
loop = asyncio.get_event_loop()
loop.run_until_complete(db_test())