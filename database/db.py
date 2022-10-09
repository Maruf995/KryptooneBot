import random
import sqlite3
from config import bot


def sql_create():
    global db, cursor
    db = sqlite3.connect("bot.sqlite3")
    cursor = db.cursor()

    if db:
        print("База данных подключена!")

    db.execute("CREATE TABLE IF NOT EXISTS anketa "
               "(id INTEGER PRIMARY KEY, "
               "username TEXT, ")
    db.commit()


async def sql_command_insert(state):
    async with state.proxy() as data:
        cursor.execute("INSERT INTO anketa VALUES (?, ?,)",
                       tuple(data.values()))
    db.commit()


async def sql_command_random(message):
    result = cursor.execute("SELECT * FROM anketa").fetchall()
    random_user = random.choice(result)
    await bot.send_photo(message.from_user.id, random_user[2],
                         caption=f"Decsription: {random_user[3]}\n")



def sql_command_all():
    user_list = cursor.execute("SELECT * FROM anketa").fetchall()
    return user_list


async def sql_command_delete(id):
    cursor.execute("DELETE FROM anketa WHERE id == ?", (id,))
    db.commit()
