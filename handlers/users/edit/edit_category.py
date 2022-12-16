from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from data.db import DBCommands
from handlers.users.commands.menu import menu, show_menu
from keyboards.inline.edit_keyboard import save_or_cancel_keyboard
from loader import dp
from states.edit_states import FSMCreateCategory, FSMDeleteCategory


async def update_storage(chat_id, storage):
    await dp.storage.update_data(chat=chat_id,
                                 category_id=storage["category_id"],
                                 parent_id=storage["parent_id"])


# Create
@dp.callback_query_handler(text_contains="edit:create")
async def create_category(call: CallbackQuery):
    await call.message.edit_text("Введите название категории:")
    await FSMCreateCategory.get_name.set()


@dp.message_handler(content_types="text", state=FSMCreateCategory.get_name)
async def name_category(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите текст:")
    await FSMCreateCategory.get_text.set()


@dp.message_handler(content_types="text", state=FSMCreateCategory.get_text)
async def text_category(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(text=message.text)
    await message.answer("Новая категория:\n"
                         f"Название: {data['name']}\n"
                         f"Текст: {message.text}\n",
                         reply_markup=save_or_cancel_keyboard())
    await FSMCreateCategory.save.set()


@dp.callback_query_handler(text_contains="save", state=FSMCreateCategory.save)
async def save_category(call: CallbackQuery, state: FSMContext):
    db = DBCommands()
    data = await state.get_data()
    storage = await dp.storage.get_data(chat=call.message.chat.id)

    name = data["name"]
    text = data["text"]

    db.create_category(name=name, text=text, parent_id=storage["category_id"])

    await call.message.edit_text("Категория добавлена")
    await state.reset_data()
    await state.reset_state()

    await update_storage(call.message.chat.id, storage)

    await show_menu(call.message, storage)


# Delete
@dp.callback_query_handler(text_contains="edit:delete")
async def delete_category(call: CallbackQuery):
    await call.message.edit_text("Вы действительно хотите удалить категорию?",
                                 reply_markup=save_or_cancel_keyboard())

    await FSMDeleteCategory.save.set()


@dp.callback_query_handler(text_contains="save", state=FSMDeleteCategory.save)
async def delete(call: CallbackQuery, state: FSMContext):
    db = DBCommands()
    chat_id = call.message.chat.id
    storage = await dp.storage.get_data(chat=chat_id)
    db.delete_category(category_id=storage['category_id'])

    await call.message.edit_text("Категория удалена")
    await state.reset_state()
    await update_storage(chat_id, storage)
    await show_menu(call.message, storage)


