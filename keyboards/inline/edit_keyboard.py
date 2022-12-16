from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


edit_menu = InlineKeyboardButton(
    text="Редактировать",
    callback_data=f"edit:manager"
    )


def edit_inline_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text=f"Добавить категорию",
            callback_data=f"edit:create"
            ),
        InlineKeyboardButton(
            text=f"Удалить категорию",
            callback_data=f"edit:delete"
        ),
        )

    return keyboard


def save_or_cancel_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text=f"Отменить",
            callback_data=f"cancel"
            ),
        InlineKeyboardButton(
            text=f"Сохранить",
            callback_data=f"save"
        ),
        )

    return keyboard