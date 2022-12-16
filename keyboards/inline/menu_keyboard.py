from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.db import DBCommands
from data.models import MenuCategories

db = DBCommands()


def menu_inline_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    categories = db.get_all(MenuCategories)
    for category in categories:
        keyboard.add(
            InlineKeyboardButton(
                text=f"{category.name}",
                callback_data=f"category:{category.id}"
                ),
            )

    return keyboard