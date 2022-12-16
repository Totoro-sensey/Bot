import logging
from aiogram import executor
from data.db import DBCommands
from data.models import Role
from loader import dp
import middlewares, handlers
from utils.notify_admins import on_startup_notify


def create_roles():
    db = DBCommands()
    role_list = ["administrator", "user"]

    for role_name in role_list:
        if not db.get(Role, name=role_name):
            db.create_role(role_name)


# noinspection PyUnusedLocal
async def on_startup(dispatcher):
    db = DBCommands()
    try:
        db.create_tables()
    except Exception as e:
        logging.info(f"Failed to create table\n{str(e)}")

    create_roles()

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
