from aiogram_dialog import DialogManager

from core import logger
from db import db_helper
from db.crud.categories import CategoryCRUD
from db.crud.pages import PageCRUD


async def category_getter(dialog_manager: DialogManager, **kwargs):
    async with db_helper.session() as session:
        all_categories = await CategoryCRUD.get_all_categories(session)
    return {
        "categories": [(category.name, str(category.id)) for category in all_categories]
    }

async def page_getter(dialog_manager: DialogManager, **kwargs):
    async with db_helper.session() as session:
        all_pages = await PageCRUD.get_all_pages(session)
    return {
        "pages": [(page.name, str(page.id)) for page in all_pages]
    }

async def cat_page_getter(dialog_manager: DialogManager, **kwargs):
    category_id = dialog_manager.dialog_data.get("category_id")
    if not category_id:
        return {"pages": []}  # гарантуємо, що "pages" завжди є

    async with db_helper.session() as session:
        cat_pages = await PageCRUD.get_cat_pages(session, category_id)
    return {
        "pages": [(page.name, str(page.id)) for page in cat_pages]
    }

    # category_id = dialog_manager.dialog_data.get('selected_category_id')
    # if not category_id:
    #     return {"articles": []}
    #
    # async with db_helper.session() as session:
    #     articles = await PageCRUD.get_cat_pages(session, category_id)
    #     return {
    #         "articles": [(a.name, a.id) for a in articles],
    #         "category_name": next(
    #             (c.name for c in await CategoryCRUD.get_all_categories(session)
    #              if c.id == category_id), ""
    #         )
    #     }
