from aiogram.dispatcher.filters.state import StatesGroup, State


class FSMCreateCategory(StatesGroup):
    get_name = State()
    get_text = State()
    save = State()


class FSMCUpdateCategory(StatesGroup):
    get_name = State()
    get_text = State()
    save = State()


class FSMDeleteCategory(StatesGroup):
    save = State()