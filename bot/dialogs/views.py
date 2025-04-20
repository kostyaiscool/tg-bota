from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from bot.dialogs.states import Wiki


async def go_clicked(callback: CallbackQuery, button: Button,
                     manager: DialogManager):
    await callback.message.answer("Going on!")

main_window = Window(
    Const("Hello, unknown person"),  # just a constant text
    Button(Const("Useless button"), on_click=go_clicked, id="nothing"),  # button with text and id
    state=Wiki.main,  # state is used to identify window between dialogs
)