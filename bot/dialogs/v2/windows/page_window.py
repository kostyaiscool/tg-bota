from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.v2.states import Wiki, Creation
from db import db_helper
from db.crud.pages import PageCRUD


class PageWindow(Window):
    def __init__(self):
        self.page_select = Select(
            Format("{item[0]}"),  # отображаемое имя
            id="page_select",
            item_id_getter=lambda item: item[1],  # page.id
            items="pages",  # ключ из getter'а
            on_click=self.choose_pages,
        )
        super().__init__(
            Const('Все страницы'),
            Button(Const('Назад'), '2', on_click=self.go_to_main),
            self.page_select,
            getter=self.pages_getter,
            state=Wiki.page
        )

    async def go_to_main(self, callback, button, dialog_manager):
        await dialog_manager.switch_to(Wiki.main)

    async def pages_getter(self, dialog_manager: DialogManager, **kwargs):
        async with db_helper.session() as session:
            all_pages = await PageCRUD.get_all_pages(session)
        return {
            "pages": [(page.name, str(page.id)) for page in all_pages]
        }

    async def choose_pages(self, callback, button, dialog_manager: DialogManager, item_id: str):
        dialog_manager.dialog_data["page_id"] = int(item_id)
        await dialog_manager.switch_to(Wiki.page_text)

class PageTextWindow(Window):
    def __init__(self):
        self.page_select = Select(
            Format("{item[0]}"),
            id="page_select",
            item_id_getter=lambda item: item[1],
            items="pages",
            on_click=self.choose_pages,
        )
        super().__init__(
            Format("<b>{page.name}</b>\n\n{page.text}"),
            # Button(Const("🔙 Назад"), id="back_to_cat", on_click=go_to_categories),
            # Button(Const("Редактировать"), id="edit", on_click=search_name),
            getter=self.page_getter,
            state=Wiki.page_text)
    async def choose_pages(self, callback, button, dialog_manager: DialogManager, item_id: str):
        dialog_manager.dialog_data["page_id"] = int(item_id)
        await dialog_manager.switch_to(Wiki.page_text)

    async def page_getter(self, dialog_manager: DialogManager, **kwargs):
        page_id = dialog_manager.dialog_data.get("page_id", "")
        async with db_helper.session() as session:
            page = await PageCRUD.get_page(session, page_id)
        return {
            "page": page
        }

class PageSearchWindow(Window):
    def __init__(self):
        self.page_select = Select(
            Format("{item[0]}"),
            id="page_select",
            item_id_getter=lambda item: item[1],
            items="pages",
            on_click=self.choose_pages,
        )
        super().__init__(
            # Const("Редактирование"),
            # MessageInput(create_text),
            state=Creation.search,
            # getter=update_page_getter,
        )
    async def choose_pages(self, callback, button, dialog_manager: DialogManager, item_id: str):
        dialog_manager.dialog_data["page_id"] = int(item_id)
        await dialog_manager.switch_to(Wiki.page_text)

page_window = PageWindow()
page_text_window = PageTextWindow()
page_search_window = PageSearchWindow()