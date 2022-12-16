from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from handlers.users.commands.menu import show_menu
from keyboards.inline.edit_keyboard import edit_inline_keyboard
from keyboards.inline.menu_keyboard import cancel_button
from loader import dp


@dp.callback_query_handler(text_contains="edit:manager")
async def edit(call: CallbackQuery):
    await call.message.edit_text("Редактирование",
                                 reply_markup=edit_inline_keyboard().add(cancel_button))


@dp.callback_query_handler(text_contains="cancel:", state=["*"])
async def edit(call: CallbackQuery, state: FSMContext):

    storage = await dp.storage.get_data(chat=call.message.chat.id)
    await state.reset_data()
    await state.reset_state()

    await dp.storage.update_data(chat=call.message.chat.id,
                                 category_id=storage["category_id"],
                                 parent_id=storage["parent_id"])

    await show_menu(call.message)
