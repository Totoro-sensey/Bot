from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


edit_menu = InlineKeyboardButton(
    text="Редактировать",
    callback_data=f"edit:manager"
    )


def edit_inline_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(
            text=f"Добавить категорию",
            callback_data=f"edit:create"
            ),
        InlineKeyboardButton(
            text=f"Удалить категорию",
            callback_data=f"edit:delete"
        ),
        InlineKeyboardButton(
            text=f"Изменить категорию",
            callback_data=f"edit:update"
        ),
        )

    return keyboard


def update_inline_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(
            text=f"Изменить название",
            callback_data=f"edit:up_name"
            ),
        InlineKeyboardButton(
            text=f"Изменить текст",
            callback_data=f"edit:up_text"
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