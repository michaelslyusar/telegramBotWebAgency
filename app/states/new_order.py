"""
WWWizards Telegram Bot - New Request FSM States
"""
from aiogram.fsm.state import State, StatesGroup

class NewOrderState(StatesGroup):
    first_name = State()
    last_name = State()
    phone = State()
    email = State()
    service = State()
    description = State()


