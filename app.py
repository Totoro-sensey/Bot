import logging
from aiogram import executor
from data.db import DBCommands
from data.models import Role, MenuCategories
from loader import dp
import middlewares, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


def create_roles():
    db = DBCommands()
    role_list = ["administrator", "user"]

    for role_name in role_list:
        if not db.get(Role, name=role_name):
            db.create_role(role_name)


def create_main_menu():
    db = DBCommands()
    if not db.get(MenuCategories, id=1):
        db.create_category(name="Главное меню")


# noinspection PyUnusedLocal
async def on_startup(dispatcher):
    db = DBCommands()
    try:
        db.create_tables()
    except Exception as e:
        logging.info(f"Failed to create table\n{str(e)}")

    create_roles()
    create_main_menu()

    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
