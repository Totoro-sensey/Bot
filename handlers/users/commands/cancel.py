from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.commands.menu import menu
from loader import dp


@dp.message_handler(commands="cancel", state=["*"])
async def cancel(message: types.Message, state: FSMContext):
    await state.reset_data()
    await state.reset_state()

    await menu(message)
