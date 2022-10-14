from aiogram import types
from loader import dp

from filters import IsPrivate
from utils.db_api import quick_commands as commands
from utils.misc import rate_limit


@rate_limit(limit=3)
@dp.message_handler(IsPrivate(), text='/start')
async def command_start(message: types.Message):
    try:
        user = await commands.select_user(message.from_user.id)
        await  message.answer(f'Привет {user.first_name}\n'
                              f'Ты уже зареаган')

    except Exception:
        await commands.add_user(user_id=message.from_user.id,
                                first_name=message.from_user.first_name,
                                last_name=message.from_user.last_name,
                                username=message.from_user.username)
        await message.answer('Ты успешно зареган')
