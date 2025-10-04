from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Select, ScrollingGroup
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.v2.states import Wiki, Creation
from db import db_helper
from db.crud.categories import CategoryCRUD
from db.crud.pages import PageCRUD
from schemas.pages import PageCreate


class CreateNameWindow(Window):
    def __init__(self):
        super().__init__(
            Const("Создать название"),
            Button(Const('Назад'), '6', on_click=self.go_back),
            MessageInput(self.create_name),
            state=Creation.create_name,
        )

    async def create_name(self, message, dialog, dialog_manager: DialogManager):
        query = message.text
        dialog_manager.dialog_data["name_input"] = query
        await dialog_manager.switch_to(Creation.create_text)

    async def go_back(self, callback, button, dialog_manager: DialogManager):
        await dialog_manager.start(Wiki.main)


class CreateTextWindow(Window):
    def __init__(self):
        super().__init__(
            Const("Создать текст"),
            Button(Const('Назад'), '5', on_click=self.go_back),
            MessageInput(self.create_text),
            state=Creation.create_text,
        )

    async def create_text(self, message, dialog, dialog_manager: DialogManager):
        query = message.text
        dialog_manager.dialog_data["text_input"] = query
        await dialog_manager.switch_to(Creation.choose_category)

    async def go_back(self, callback, button, dialog_manager: DialogManager):
        await dialog_manager.switch_to(Creation.create_name)


class ChooseCategoryWindow(Window):
    # def __init__(self):
    #     super().__init__(
    #         Const("Выберите категории"),
    #         MessageInput(self.create_text),
    #         state=Creation.create_text,
    #     )

    def __init__(self):
        self.category_select = Select(
            Format("{item[0]}"),
            id="category_select",
            item_id_getter=lambda item: item[1],
            items="categories",
            on_click=self.choose_categories,
        )
        self.category_scrolling = ScrollingGroup(
            self.category_select,
            id="categories",
            width=1,
            height=6,
        )
        super().__init__(
            Const("Выберите категорию среди розию"),
            Button(Const('Назад'), '2', on_click=self.go_to_main),
            self.category_scrolling,
            getter=self.category_getter,
            state=Creation.choose_category,

        )

    async def choose_categories(self, callback, button, dialog_manager: DialogManager, item_id: str):
        dialog_manager.dialog_data["category_id"] = int(item_id)
        # await dialog_manager.switch_to(Wiki.cat_page)
        async with db_helper.session() as session:
            page_data = PageCreate(
                name=dialog_manager.dialog_data["name_input"],
                text=dialog_manager.dialog_data["text_input"],
                category_id=dialog_manager.dialog_data["category_id"],
                author_id=6298150733
            )
            new_page = await PageCRUD.create_or_update(session, page_data=page_data)
            dialog_manager.dialog_data["page_id"] = new_page[0].id

        await dialog_manager.switch_to(Creation.preview)

    async def category_getter(self, dialog_manager: DialogManager, **kwargs):
        async with db_helper.session() as session:
            all_categories = await CategoryCRUD.get_all_categories(session)
        return {
            "categories": [(category.name, str(category.id)) for category in all_categories]
        }

    async def go_to_main(self, callback, button, dialog_manager: DialogManager):
        await dialog_manager.switch_to(Creation.create_text)

class PreviewWindow(Window):
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
            Button(Const('Назад к категориям'), '2', on_click=self.go_to_categories),
            # Button(Const("Редактировать"), id="edit", on_click=search_name),
            getter=self.page_getter,
            state=Creation.preview)

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
        await dialog_manager.start(Wiki.category)

name_window = CreateNameWindow()
text_window = CreateTextWindow()
category_choose_window = ChooseCategoryWindow()
preview_window = PreviewWindow()
