from aiogram.dispatcher.filters.state import StatesGroup, State

class admin(StatesGroup):
    del_user = State()
    add_link = State()
    del_link = State()
    del_loop = State()