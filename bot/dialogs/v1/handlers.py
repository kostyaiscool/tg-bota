from aiogram_dialog import DialogManager
from sqlalchemy.ext.asyncio import AsyncSession

from bot.dialogs.states import Wiki, Creation
from db import db_helper
from db.crud.categories import CategoryCRUD
from db.crud.pages import PageCRUD
from db.crud.user import TelegramUserCRUD
from db.models.pages import Page
from schemas.pages import Pages, PageCreate


async def choose_categories(callback, button, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data["category_id"] = int(item_id)
    await dialog_manager.switch_to(Wiki.cat_page)


async def choose_pages(callback, button, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data["page_id"] = int(item_id)
    await dialog_manager.switch_to(Wiki.page_text)


async def go_to_categories(callback, button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(Wiki.category)


async def go_to_pages(callback, button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(Wiki.page)


async def go_to_main(callback, button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(Wiki.main)


async def go_to_search(callback, button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(Wiki.search)


async def find_page(message, dialog, dialog_manager: DialogManager):
    query = message.text
    dialog_manager.dialog_data["search_input"] = query
    await dialog_manager.switch_to(Creation.search_page)


async def create_name(message, dialog, dialog_manager: DialogManager):
    query = message.text
    dialog_manager.dialog_data["name_input"] = query
    await dialog_manager.switch_to(Creation.create_text)


async def create_text(message, dialog, dialog_manager: DialogManager):
    query = message.text
    dialog_manager.dialog_data["text_input"] = query
    await dialog_manager.switch_to(Creation.choose_category)


async def choose_category(callback, button, dialog_manager: DialogManager, item_id):
    # dialog_manager.dialog_data["category_id"] = int(item_id)
    name = dialog_manager.dialog_data.get("name_input", "")
    text = dialog_manager.dialog_data.get("text_input", "")
    category_id = int(item_id)
    async with db_helper.session() as session:
        print('Недавно Марку исполнилась 4 года, ')
        print(name, ' ', text, ' ', category_id)
        category = await CategoryCRUD.get_category(session, category_id)
        new_page, status = await PageCRUD.create_or_update(session,
            PageCreate(name=name, text=text, category_id=category, author_id=6298150733)
        )
    if not status:
        dialog_manager.dialog_data["new_page"] = new_page.id
        await dialog_manager.switch_to(Creation.preview)


async def preview(dialog_manager: DialogManager, message):
    name = dialog_manager.dialog_data.get("name_input", "❌ без названия")
    text = dialog_manager.dialog_data.get("text_input", "❌ без текста")
    category_id = dialog_manager.dialog_data.get("category_id", "❌ не выбрана")

    preview_message = (
        f"<b>🔍 Предпросмотр страницы</b>\n\n"
        f"<b>Название:</b> {name}\n"
        f"<b>Категория ID:</b> {category_id}\n\n"
        f"<b>Текст:</b>\n{text}"
    )

    await message.answer(preview_message, parse_mode="HTML")
    # Можно вытянуть имя категории по ID из базы, если нужно
    # category = await get_category_name(category_id)

    # После предпросмотра можешь перевести в состояние подтверждения/сохранения
    # await dialog_manager.switch_to(Wiki.confirm)
async def search_name(message, dialog, dialog_manager: DialogManager):
    query = message.text
    dialog_manager.dialog_data["search_name"] = query
    await dialog_manager.switch_to(Creation.editing)