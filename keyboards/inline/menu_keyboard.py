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


def menu_inline_keyboard(obj_list, page_number, isPages) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    for category in obj_list:
        keyboard.add(
            InlineKeyboardButton(
                text=f"{category.name}",
                callback_data=f"category:{category.id}"
                ),
            )
    if isPages:
        keyboard.row_width = 3
        keyboard.add(
            InlineKeyboardButton(
                text=f"🔙",
                callback_data=f"previous"
            ),
            InlineKeyboardButton(
                text=f"{page_number}",
                callback_data=f"page_number"
            ),
            InlineKeyboardButton(
                text=f"🔜",
                callback_data=f"next"
            ),
            )

    return keyboard