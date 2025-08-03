from aiogram_dialog import DialogManager
from sqlalchemy.ext.asyncio import AsyncSession

from bot.dialogs.states import Wiki
from db import db_helper
from db.crud.categories import CategoryCRUD
from db.crud.pages import PageCRUD


async def category_getter(dialog_manager: DialogManager, **kwargs):
    async with db_helper.session() as session:
        all_categories = await CategoryCRUD.get_all_categories(session)
    return {
        "categories": [(category.name, str(category.id)) for category in all_categories]
    }

async def pages_getter(dialog_manager: DialogManager, **kwargs):
    async with db_helper.session() as session:
        all_pages = await PageCRUD.get_all_pages(session)
    return {
        "pages": [(page.name, str(page.id)) for page in all_pages]
    }

async def cat_page_getter(dialog_manager: DialogManager, **kwargs):
    category_id = dialog_manager.dialog_data.get("category_id", "")
    async with db_helper.session() as session:
        cat_pages = await PageCRUD.get_cat_pages(session, category_id)
    return {
        "pages": [(page.name, str(page.id)) for page in cat_pages]
    }

async def page_getter(dialog_manager: DialogManager, **kwargs):
    page_id = dialog_manager.dialog_data.get("page_id", "")
    async with db_helper.session() as session:
        page = await PageCRUD.get_page(session, page_id)
    return {
        "page": page
    }

async def page_search_getter(dialog_manager: DialogManager, **kwargs):
    search = dialog_manager.dialog_data.get("search_input", "")
    # search = "Два каннибала пили, а закусил только один"
    async with db_helper.session() as session:
        pages = await PageCRUD.get_page_name(session, search)
    return {
        "pages": [(page.name, str(page.id)) for page in pages]
    }
async def confirm(callback, button, dialog_manager: DialogManager):
    name = dialog_manager.dialog_data.get("name_input", "")
    text = dialog_manager.dialog_data.get("text_input", "")
    category_id = dialog_manager.dialog_data.get("category_id", "")
    print(type(category_id), '<- Я геометрию ненавижу')
    # await PageCRUD.create_or_update(AsyncSession, [name, text, category_id])
    await dialog_manager.switch_to(Wiki.main)

async def new_page_getter(dialog_manager: DialogManager, **kwargs):
    page_id = dialog_manager.dialog_data.get("new_page", "")
    async with db_helper.session() as session:
        page = await PageCRUD.get_page(session, page_id)
    return {
        "page": page
    }
async def update_page_getter(dialog_manager: DialogManager, **kwargs):
    page_id = dialog_manager.dialog_data.get("update_page", "")
    async with db_helper.session() as session:
        page = await PageCRUD.get_page(session, page_id)
    return {
        "page": page
    }