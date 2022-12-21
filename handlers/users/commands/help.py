from aiogram import types

from loader import dp


@dp.message_handler(commands="help", state=["*"])
async def help(message: types.Message):
    await message.answer("Доступные команды:\n"
                         "/start - Запустить бота\n"
                         "/menu - Вывести меню\n"
                         "/help - Вывести справку\n"
                         "/cancel - Экстренное завершение\n")
