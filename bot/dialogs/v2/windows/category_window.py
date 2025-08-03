from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.v2.states import Wiki
from db import db_helper
from db.crud.categories import CategoryCRUD
from db.crud.pages import PageCRUD


class CategoryWindow(Window):
    def __init__(self):
        self.category_select=Select(
                Format("{item[0]}"),
                id="category_select",
                item_id_getter=lambda item: item[1],
                items="categories",
                on_click=self.choose_categories,
            )
        super().__init__(
            Const("Выберите категорию среди навоза"),
            # Button(Const('Назад'), '2', on_click=go_to_main),
            self.category_select,
            getter=self.category_getter,
            state=Wiki.category,

        )

    async def choose_categories(self, callback, button, dialog_manager: DialogManager, item_id: str):
        dialog_manager.dialog_data["category_id"] = int(item_id)
        await dialog_manager.switch_to(Wiki.cat_page)

    async def category_getter(self, dialog_manager: DialogManager, **kwargs):
        async with db_helper.session() as session:
            all_categories = await CategoryCRUD.get_all_categories(session)
        return {
            "categories": [(category.name, str(category.id)) for category in all_categories]
            }


class CatPageWindow(Window):
    def __init__(self):
        self.page_select = Select(
            Format("{item[0]}"),
            id="page_select",
            item_id_getter=lambda item: item[1],
            items="pages",
            on_click=self.choose_pages,
        )
        super().__init__(
            Const("Выбрать страницы"),
            self.page_select,
            getter=self.cat_page_getter,
            state=Wiki.cat_page,
        )

    async def cat_page_getter(self, dialog_manager: DialogManager, **kwargs):
        category_id = dialog_manager.dialog_data.get("category_id", "")
        async with db_helper.session() as session:
            cat_pages = await PageCRUD.get_cat_pages(session, category_id)
        print("2022-ицированние началось ", cat_pages, type(cat_pages))
        return {
            "pages": [(page.name, str(page.id)) for page in cat_pages]
        }

    async def choose_pages(self, callback, button, dialog_manager: DialogManager, item_id: str):
        dialog_manager.dialog_data["page_id"] = int(item_id)
        await dialog_manager.switch_to(Wiki.page_text)

category_window = CategoryWindow()
cat_page_window = CatPageWindow()