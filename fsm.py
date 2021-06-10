from aiogram.dispatcher.filters.state import State, StatesGroup

class DataInput(StatesGroup):
    state_length = State()
    state_settings = State()

class AdminInput(StatesGroup):
    state_settings = State()