from aiogram import types
from aiogram.types import CallbackQuery
from data.db import DBCommands
from data.models import MenuCategories
from keyboards.inline.edit_keyboard import edit_menu
from keyboards.inline.menu_keyboard import menu_inline_keyboard, back_to_menu
from loader import dp
from utils.paginator import Paginator

db = DBCommands()


async def show_menu(message):
    storage = await dp.storage.get_data(chat=message.chat.id)
    category = db.get(MenuCategories, id=storage["category_id"])
    paginator = Paginator(category.Children, page_number=storage["page_number"])
    page = paginator.get_page(category.Children, page_number=storage["page_number"])
    keyboard = menu_inline_keyboard(obj_list=page,
                                    page_number=paginator.page_number,
                                    isPages=paginator.diapason > 1)
    if db.get_user(message.chat.id).Role.name == "administrator":
        keyboard.add(edit_menu)
    if category.parent_id:
        keyboard.add(back_to_menu)

    await message.edit_text(text=f"{category.name}\n"
                                 f"{category.text}",
                                 reply_markup=keyboard)


@dp.message_handler(commands="menu")
async def menu(message: types.Message):
    category = db.get(MenuCategories, id=1)

    paginator = Paginator(category.Children)
    page = paginator.get_page(category.Children)
    keyboard = menu_inline_keyboard(obj_list=page,
                                    page_number=paginator.page_number,
                                    isPages=paginator.diapason > 1)

    if db.get_user(message.chat.id).Role.name == "administrator":
        keyboard.add(edit_menu)

    await dp.storage.update_data(chat=message.chat.id,
                                 category_id=1,
                                 parent_id=0,
                                 page_number=1)

    await message.answer(text="Главное меню", reply_markup=keyboard)


@dp.callback_query_handler(text_contains="category:")
async def get_category(call: CallbackQuery):
    category_id = call.data.split(":")[-1]

    storage = await dp.storage.get_data(chat=call.message.chat.id)
    if storage != {}:
        await dp.storage.update_data(chat=call.message.chat.id,
                                     category_id=category_id,
                                     parent_id=storage["category_id"],
                                     page_number=1)

        category = db.get(MenuCategories, id=category_id)

        paginator = Paginator(category.Children)
        page = paginator.get_page(category.Children)

        keyboard = menu_inline_keyboard(obj_list=page,
                                        page_number=paginator.page_number,
                                        isPages=paginator.diapason > 1)

        if db.get_user(call.from_user.id).Role.name == "administrator":
            keyboard.add(edit_menu)
        if category.parent_id:
            keyboard.add(back_to_menu)

        await call.message.edit_text(text=f"{category.name}\n"
                                     f"{category.text}",
                                     reply_markup=keyboard)
    else:
        await call.message.delete()
        await menu(call.message)


@dp.callback_query_handler(text_contains="back")
async def get_category(call: CallbackQuery):
    storage = await dp.storage.get_data(chat=call.message.chat.id)

    if storage != {}:
        category = db.get(MenuCategories, id=storage["parent_id"])

        paginator = Paginator(category.Children, page_number=storage["page_number"])
        page = paginator.get_page(category.Children, page_number=storage["page_number"])

        await dp.storage.update_data(chat=call.message.chat.id,
                                     category_id=category.id,
                                     parent_id=category.parent_id)

        keyboard = menu_inline_keyboard(obj_list=page,
                                        page_number=paginator.page_number,
                                        isPages=paginator.diapason > 1)

        if db.get_user(call.from_user.id).Role.name == "administrator":
            keyboard.add(edit_menu)
        if category.parent_id:
            keyboard.add(back_to_menu)

        text = f"{category.name}\n"
        if category.text:
            text += category.text

        await call.message.edit_text(text=text, reply_markup=keyboard)
    else:
        await call.message.delete()
        await menu(call.message)


@dp.callback_query_handler(text_contains="next")
async def get_category(call: CallbackQuery):
    storage = await dp.storage.get_data(chat=call.message.chat.id)

    if storage != {}:
        category = db.get(MenuCategories, id=storage["category_id"])
        page_number = storage["page_number"] + 1
        paginator = Paginator(category.Children, page_number=page_number)
        page = paginator.get_page(category.Children, page_number=page_number)
        if paginator.has_next(page_number=page_number):
            keyboard = menu_inline_keyboard(obj_list=page,
                                            page_number=paginator.page_number,
                                            isPages=paginator.diapason > 1)

            await dp.storage.update_data(chat=call.message.chat.id,
                                         category_id=category.id,
                                         parent_id=storage["parent_id"],
                                         page_number=page_number)

            if db.get_user(call.from_user.id).Role.name == "administrator":
                keyboard.add(edit_menu)
            if category.parent_id:
                keyboard.add(back_to_menu)

            text = f"{category.name}\n"
            if category.text:
                text += category.text

            await call.message.edit_text(text=text, reply_markup=keyboard)
        else:
            await call.answer(text="Вы находитесь на последней странице!")
    else:
        await call.message.delete()
        await menu(call.message)


@dp.callback_query_handler(text_contains="previous")
async def get_category(call: CallbackQuery):
    storage = await dp.storage.get_data(chat=call.message.chat.id)

    if storage != {}:
        category = db.get(MenuCategories, id=storage["category_id"])
        page_number = storage["page_number"] - 1
        paginator = Paginator(category.Children, page_number=page_number)
        page = paginator.get_page(category.Children, page_number=page_number)
        if paginator.has_previous(page_number=page_number):

            keyboard = menu_inline_keyboard(obj_list=page,
                                            page_number=paginator.page_number,
                                            isPages=paginator.diapason > 1)

            await dp.storage.update_data(chat=call.message.chat.id,
                                         category_id=category.id,
                                         parent_id=storage["parent_id"],
                                         page_number=page_number)

            if db.get_user(call.from_user.id).Role.name == "administrator":
                keyboard.add(edit_menu)
            if category.parent_id:
                keyboard.add(back_to_menu)

            text = f"{category.name}\n"
            if category.text:
                text += category.text

            await call.message.edit_text(text=text, reply_markup=keyboard)
        else:
            await call.answer(text="Вы находитесь на первой странице!")
    else:
        await call.message.delete()
        await menu(call.message)
