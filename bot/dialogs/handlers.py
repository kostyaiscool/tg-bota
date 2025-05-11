from aiogram_dialog import DialogManager

from bot.dialogs.states import Wiki
from db import db_helper
from db.crud.pages import PageCRUD


async def choose_categories(callback, button, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data["category_id"] = int(item_id)
    await dialog_manager.switch_to(Wiki.page)
    # async with db_helper.session() as session:
    #     cat_pages = await PageCRUD.get_cat_pages(session, int(item_id))
    #     await callback.answer(cat_pages)
    # await callback.answer(f'вы выбрали категорию среди роз: {item_id}')