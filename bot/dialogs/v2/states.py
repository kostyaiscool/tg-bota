from aiogram.filters.state import StatesGroup, State

class Wiki(StatesGroup):
    main = State()
    category = State()
    page = State()
    cat_page = State()
    page_text = State()
    search = State()
    search_page = State()

class Creation(StatesGroup):
    create_name = State()
    create_text = State()
    choose_category = State()
    preview = State()
    search = State()
    editing = State()