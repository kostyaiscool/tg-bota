from aiogram_dialog import Window, DialogManager, StartMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Select, ScrollingGroup
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
        self.page_scrolling = ScrollingGroup(
            self.page_select,
            id="pages",
            width=1,
            height=6,
        )
        super().__init__(
            Const('Все страницы'),
            Button(Const('Назад'), '2', on_click=self.go_to_main),
            self.page_scrolling,
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
            Button(Const('Редактировать'), '7'),
            Button(Const('Назад к категориям'), '2', on_click=self.go_to_categories),
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

    async def go_to_categories(self, callback, button, dialog_manager: DialogManager):
        await dialog_manager.switch_to(Wiki.category)


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
            Const("Введите текст для поиска:"),
            MessageInput(self.find_page),
            # getter=page_search_getter,
            state=Wiki.search)

    async def choose_pages(self, callback, button, dialog_manager: DialogManager, item_id: str):
        dialog_manager.dialog_data["page_id"] = int(item_id)
        await dialog_manager.switch_to(Wiki.page_text)

    async def page_search_getter(self, dialog_manager: DialogManager, **kwargs):
        search = dialog_manager.dialog_data.get("search_input", "")
        # search = "Два каннибала пили, а закусил только один"
        async with db_helper.session() as session:
            pages = await PageCRUD.get_page_name(session, search)
        return {
            "pages": [(page.name, str(page.id)) for page in pages]}

    async def find_page(self, message, dialog, dialog_manager: DialogManager):
        query = message.text
        dialog_manager.dialog_data["search_input"] = query

        # await dialog_manager.start(Wiki.search_page, mode=StartMode.RESET_STACK)
        await dialog_manager.switch_to(Wiki.search_page)

class PageSearchedWindow(Window):
    def __init__(self):
        self.page_select = Select(
            Format("{item[0]}"),  # отображаемое имя
            id="page_select",
            item_id_getter=lambda item: item[1],  # page.id
            items="pages",  # ключ из getter'а
            on_click=self.choose_pages,
        )
        self.page_scrolling = ScrollingGroup(
            self.page_select,
            id="pages",
            width=1,
            height=6,
        )
        super().__init__(
            Const("Результаты поиска"),
            self.page_scrolling,
            getter=self.page_search_getter,
            state=Wiki.search_page,
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

    async def page_search_getter(self, dialog_manager: DialogManager, **kwargs):
        search = dialog_manager.dialog_data.get("search_input", "")
        # search = "Два каннибала пили, а закусил только один"
        async with db_helper.session() as session:
            pages = await PageCRUD.get_page_name(session, search)
        # if not pages:
        #     return {"pages": "Страниц не найдено, лее брат:("}
        # else:
        return {"pages": [(page.name, str(page.id)) for page in pages]}


page_window = PageWindow()
page_text_window = PageTextWindow()
page_search_window = PageSearchWindow()
page_searched_window = PageSearchedWindow()