from aiogram import types
from data.db import DBCommands
from handlers.users.commands.menu import menu
from loader import dp

db = DBCommands()


@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer(f"Приветствую Вас, {message.from_user.full_name}!\n"
                         f"Вы можете выбрать в меню интересующую Вас категорию🌑")
    if not db.get_user(message.from_user.id):
        db.create_user(message.from_user.id, message.from_user.full_name, message.from_user.username, 2)
        await message.answer("Вы были зарегистрированы")

    await menu(message)
