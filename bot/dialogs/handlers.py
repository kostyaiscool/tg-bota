from aiogram_dialog import DialogManager

from bot.dialogs.states import Wiki
from db import db_helper
from db.crud.pages import PageCRUD


async def choose_categories(callback, button, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data["category_id"] = int(item_id)
    await dialog_manager.switch_to(Wiki.cat_page)

async def choose_pages(callback, button, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data["page_id"] = int(item_id)
    async with db_helper.session() as session:
        page = await PageCRUD.get_page(session, int(item_id))
        await callback.message.answer(
            f"<b>{page.name}</b>\n\n{page.text}",
            parse_mode="HTML"
        )

    # await dialog_manager.switch_to(Wiki.main)

async def go_to_categories(callback, button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(Wiki.category)

async def go_to_pages(callback, button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(Wiki.page)

async def go_to_main(callback, button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(Wiki.main)