import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup
from data.db import DBCommands
from data.models import MenuCategories
from handlers.users.commands.menu import show_menu
from keyboards.inline.edit_keyboard import save_or_cancel_keyboard, update_inline_keyboard
from keyboards.inline.menu_keyboard import cancel_button
from loader import dp
from states.edit_states import FSMCreateCategory, FSMDeleteCategory, FSMCUpdateCategory


async def delete_previous_keyboard(message):
    # Удаление кнопки у предыдущего сообщения
    previous_message = message
    previous_message.message_id = message.message_id - 1
    try:
        await previous_message.delete_reply_markup()
    except:
        logging.info("Cообщение без кнопки.")


#  __________________Create___________________
@dp.callback_query_handler(text_contains="edit:create")
async def create_category(call: CallbackQuery):
    await call.message.edit_text("Введите название категории:",
                                 reply_markup=InlineKeyboardMarkup().add(cancel_button))
    await FSMCreateCategory.get_name.set()


@dp.message_handler(content_types="text", state=FSMCreateCategory.get_name)
async def name_category(message: types.Message, state: FSMContext):
    await delete_previous_keyboard(message)
    await state.update_data(name=message.text)
    await message.answer("Введите текст:",
                         reply_markup=InlineKeyboardMarkup().add(cancel_button))
    await FSMCreateCategory.get_text.set()


@dp.message_handler(content_types="text", state=FSMCreateCategory.get_text)
async def text_category(message: types.Message, state: FSMContext):
    await delete_previous_keyboard(message)
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
                                 parent_id=storage["parent_id"],
                                 page_number=storage["page_number"])

    await show_menu(call.message)


# __________________Delete___________________
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
                                 parent_id=category.parent_id,
                                 page_number=storage["page_number"])
    await show_menu(call.message)


# __________________Update___________________
@dp.callback_query_handler(text_contains="edit:update")
async def update_category(call: CallbackQuery):
    await call.message.edit_text("Что хотите изменить:",
                                 reply_markup=update_inline_keyboard().add(cancel_button))


@dp.callback_query_handler(text_contains="edit:up_name")
async def update_category(call: CallbackQuery):
    await call.message.edit_text("Введите новое название категории:")
    await FSMCUpdateCategory.get_name.set()


@dp.message_handler(content_types="text", state=FSMCUpdateCategory.get_name)
async def name_category(message: types.Message, state: FSMContext):
    db = DBCommands()
    await delete_previous_keyboard(message)

    await state.update_data(name=message.text)
    storage = await dp.storage.get_data(chat=message.chat.id)
    category = db.get(MenuCategories, id=storage["category_id"])
    await message.answer(f"Прошлое название: {category.name}\n"
                         f"Новое название: {message.text}",
                         reply_markup=save_or_cancel_keyboard())
    await FSMCUpdateCategory.save.set()


@dp.callback_query_handler(text_contains="edit:up_text")
async def update_category(call: CallbackQuery):
    await call.message.edit_text("Введите новый текст категории:")
    await FSMCUpdateCategory.get_text.set()


@dp.message_handler(content_types="text", state=FSMCUpdateCategory.get_text)
async def text_category(message: types.Message, state: FSMContext):
    db = DBCommands()
    await delete_previous_keyboard(message)

    await state.update_data(text=message.text)
    storage = await dp.storage.get_data(chat=message.chat.id)
    category = db.get(MenuCategories, id=storage["category_id"])
    await message.answer(f"Прошлый текст: {category.text}\n"
                         f"Новый текст: {message.text}",
                         reply_markup=save_or_cancel_keyboard())
    await FSMCUpdateCategory.save.set()


@dp.callback_query_handler(text_contains="save", state=FSMCUpdateCategory.save)
async def save_category(call: CallbackQuery, state: FSMContext):
    db = DBCommands()
    data = await state.get_data()
    storage = await dp.storage.get_data(chat=call.message.chat.id)
    try:
        name = data["name"]
        db.update_category(name=name, category_id=storage["category_id"])
    except:
        text = data["text"]
        db.update_category(text=text, category_id=storage["category_id"])

    await call.message.edit_text("Категория обновлена")
    await state.reset_data()
    await state.reset_state()

    await dp.storage.update_data(chat=call.message.chat.id,
                                 category_id=storage["category_id"],
                                 parent_id=storage["parent_id"],
                                 page_number=storage["page_number"])

    await show_menu(call.message)
