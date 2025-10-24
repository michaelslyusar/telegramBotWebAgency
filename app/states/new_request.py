"""
WWWizards Telegram Bot - New Request FSM States
"""
from aiogram.fsm.state import State, StatesGroup


class NewRequestState(StatesGroup):
    first_name = State()
    last_name = State()
    email = State()
    service = State()
    description = State()


