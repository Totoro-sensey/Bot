from aiogram import types

from data.db import DBCommands
from data.models import User
from keyboards.inline.edit_keyboard import edit_menu
from keyboards.inline.menu_keyboard import menu_inline_keyboard
from loader import dp, bot

db = DBCommands()


@dp.message_handler(commands="menu")
async def menu(message: types.Message):
    keyboard = menu_inline_keyboard()
    if db.get_user(message.from_user.id).Role.name == "administrator":
        keyboard.add(edit_menu)
    await message.answer(
        text="Главное меню",
        reply_markup=keyboard,
    )
