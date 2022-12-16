from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup
from data.db import DBCommands
from data.models import MenuCategories
from handlers.users.commands.menu import menu, show_menu
from keyboards.inline.edit_keyboard import save_or_cancel_keyboard
from keyboards.inline.menu_keyboard import cancel_button
from loader import dp
from states.edit_states import FSMCreateCategory, FSMDeleteCategory


# Create
@dp.callback_query_handler(text_contains="edit:create")
async def create_category(call: CallbackQuery):
    await call.message.edit_text("Введите название категории:",
                                 reply_markup=InlineKeyboardMarkup().add(cancel_button))
    await FSMCreateCategory.get_name.set()


@dp.message_handler(content_types="text", state=FSMCreateCategory.get_name)
async def name_category(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите текст:",
                         reply_markup=InlineKeyboardMarkup().add(cancel_button))
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

    await dp.storage.update_data(chat=call.message.chat.id,
                                 category_id=storage["category_id"],
                                 parent_id=storage["parent_id"])

    await show_menu(call.message)


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
    category = db.get(MenuCategories, id=storage["parent_id"])
    db.delete_category(category_id=storage['category_id'])

    await call.message.edit_text("Категория удалена")
    await state.reset_state()
    await dp.storage.update_data(chat=chat_id,
                                 category_id=category.id,
                                 parent_id=category.parent_id)
    await show_menu(call.message)


