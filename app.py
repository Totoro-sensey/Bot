import logging

from aiogram import Bot
import middlewares, filters, handlers
from aiogram.utils import executor
from aiohttp import web

from data.db import DBCommands
from loader import dp
from utils.notify_admins import on_startup_notify


# noinspection PyUnusedLocal
async def on_startup(dispatcher):
    db = DBCommands()
    try:
        await db.create_tables()
    except Exception as e:
        logging.info(f"Failed to create table\n{str(e)}")

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


async def on_shutdown(app: web.Application):
    app_bot: Bot = app['bot']
    await app_bot.close()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
