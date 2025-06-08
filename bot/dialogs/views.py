from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Select, Button
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.getters import category_getter, page_getter, cat_page_getter, pages_getter
from bot.dialogs.handlers import choose_categories, go_to_categories, go_to_pages, go_to_main, choose_pages, \
    go_to_search
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
    on_click=choose_pages,
)

main_window = Window(
    Const("Добро пожаловаться вам. Служить великий Китай😡"),
    Button(Const('Категории'), '1', on_click=go_to_categories),
    Button(Const('Страницы'), '2', on_click=go_to_pages),
    Button(Const('Поиск'), '3', on_click=go_to_search),
    Button(Const('Создать'), '4'),
    state=Wiki.main,
)

category_window = Window(
    Const("Выберите категорию среди навоза"),
    Button(Const('Назад'), '2', on_click=go_to_main),
    category_select,
    getter=category_getter,
    state=Wiki.category,
)
page_window = Window(
    Const('Все страницы'),
    Button(Const('Назад'), '2', on_click=go_to_main),
    page_select,
    getter=pages_getter,
    state=Wiki.page
)
cat_page_window = Window(
    Const("Выбрать страницы"),
    page_select,
    getter=cat_page_getter,
    state=Wiki.cat_page,
)
search = Window(
    Const("Введите текст для поиска:"),
    TextInput(id="search_input"),
    # getter=get_page_name,
    state=Wiki.search,
)