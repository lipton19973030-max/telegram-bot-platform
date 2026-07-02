from aiogram.fsm.state import State, StatesGroup


class OrderStates(StatesGroup):
    choosing_service = State()
    entering_description = State()
    confirming = State()