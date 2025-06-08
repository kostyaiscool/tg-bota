from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Select
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.getters import category_getter, page_getter, cat_page_getter
from bot.dialogs.handlers import choose_categories
from bot.dialogs.states import Wiki

category_select = Select(
    Format("{item[0]}"),
    id="category_select",
    item_id_getter=lambda item: item[1],
    items="categories",
    on_click=choose_categories,
)

page_select = Select(
    Format("{item[0]}"),
    id="page_select",
    item_id_getter=lambda item: item[1],
    items="pages",
    on_click=choose_categories,
)

main_window = Window(
    Const("Выберите категорию среди навоза"),
    category_select,
    getter=category_getter,
    state=Wiki.main,
)
page_window = Window(
    Const("Выбрать страницы"),
    page_select,
    getter=cat_page_getter,
    state=Wiki.page,
)
