from aiogram.filters.state import StatesGroup, State

class Wiki(StatesGroup):
    main = State()
    page = State()