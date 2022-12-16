from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.db import DBCommands
from data.models import MenuCategories

db = DBCommands()

back_to_menu = InlineKeyboardButton(
    text="Назад",
    callback_data=f"back:"
    )

cancel_button = InlineKeyboardButton(
    text="Отмена",
    callback_data=f"cancel:"
    )


def menu_inline_keyboard(category_id) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    categories = db.get_all(MenuCategories, parent_id=category_id)
    for category in categories:
        keyboard.add(
            InlineKeyboardButton(
                text=f"{category.name}",
                callback_data=f"category:{category.id}"
                ),
            )

    return keyboard