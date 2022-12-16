from aiogram.types import CallbackQuery

from keyboards.inline.edit_keyboard import edit_inline_keyboard
from loader import dp


@dp.callback_query_handler(text_contains="edit:manager")
async def edit(call: CallbackQuery):
    await call.message.edit_text("Редактирование",
                                 reply_markup=edit_inline_keyboard())

