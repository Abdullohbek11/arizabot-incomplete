from aiogram.fsm.state import StatesGroup, State

class newariza(StatesGroup):
    name = State()
    age = State()
    phone = State()
    job = State()
    goal = State()
    verify = State()
