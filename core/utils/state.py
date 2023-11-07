from aiogram.fsm.state import State, StatesGroup




class State(StatesGroup):
    initial = State()
    set_name = State()
    set_week = State()
    set_day = State()
    set_time = State()
    set_confirm = State()
    help_me = State()
    cancel_me = State()