from aiogram.filters.state import StatesGroup, State

class Wiki(StatesGroup):
    main = State()
    category = State()
    page = State()
    cat_page = State()
    page_text = State()