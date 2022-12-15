from aiogram import types

from data.db import DBCommands
from loader import dp

db = DBCommands()
@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer(f"Приветствую Вас, {message.from_user.full_name}!\n"
                         f"Я чат-бот.\n")
    if not db.get_user(message.from_user.username):
        db.create_user(message.from_user.username, 21)
        await message.answer("Вы были зарегистрированы")
