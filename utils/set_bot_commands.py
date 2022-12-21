from aiogram import types


async def set_default_commands(dp):
    commands = [
                types.BotCommand("start", "Запустить бота"),
                types.BotCommand("menu", "Вывести меню"),
                types.BotCommand("help", "Вывести справку"),
                types.BotCommand("cancel", "Экстренное завершение"),
                ]

    await dp.bot.set_my_commands(commands)
