"""
WWWizards Telegram Bot - Order FSM States
"""
from aiogram.fsm.state import State, StatesGroup


class OrderStates(StatesGroup):
    """Order quiz states."""
    
    # Waiting for text input answer
    WAITING_TEXT_ANSWER = State()
    
    # Waiting for confirmation
    WAITING_CONFIRMATION = State()
    
    # Order completed
    ORDER_COMPLETED = State()

