from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Select, Button
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.getters import category_getter, page_getter, cat_page_getter, pages_getter, page_search_getter, \
    confirm, new_page_getter
from bot.dialogs.handlers import choose_categories, go_to_categories, go_to_pages, go_to_main, choose_pages, \
    go_to_search, find_page, create_name, create_text, choose_category
from bot.dialogs.states import Wiki, Creation

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
category_choosing = Select(
    Format("{item[0]}"),
    id="category_select",
    item_id_getter=lambda item: item[1],
    items="categories",
    on_click=choose_category,
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

search_window = Window(
    Const("Введите текст для поиска:"),
    MessageInput(find_page),
    # getter=page_search_getter,
    state=Wiki.search)

show_page_text = Window(
    Const("Выбрать страницы"),
    Button(Const('Назад'), '2', on_click=go_to_main),
    page_select,
    getter=cat_page_getter,
    state=Wiki.cat_page)

page_text_window = Window(
    Format("<b>{page.name}</b>\n\n{page.text}"),
    Button(Const("🔙 Назад"), id="back_to_cat", on_click=go_to_categories),
    getter=page_getter,
    state=Wiki.page_text
)
search_page_window = Window(
    Const("Результаты поиска"),
    page_select,
    getter=page_search_getter,
    state=Wiki.search_page,
)
create_name_window = Window(
    Const("Создать название"),
    MessageInput(create_name),
    state=Creation.create_name,
)
create_text_window = Window(
    Const("Создать текст"),
    MessageInput(create_text),
    state=Creation.create_text,
)
choose_category_window = Window(
    Const("Выбрать категории"),
    category_choosing,
    getter=category_getter,
    state=Creation.choose_category,
)
preview_window = Window(
    Const("Просмотр"),
    Format("<b>{page.name}</b>\n\n{page.text}"),
    Button(Const("Подтвердить"), id="confirm", on_click=confirm),
    getter=new_page_getter,
    state=Creation.preview
)