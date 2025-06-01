from aiogram_dialog import DialogManager
from bot.dialogs.states import Wiki

async def choose_categories(callback, button, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data["category_id"] = int(item_id)
    await dialog_manager.switch_to(Wiki.page)

async def show_page(callback, button, dialog_manager: DialogManager, item_id: str):
    await callback.answer(f"Ви вибрали статтю з ID: {item_id}")
