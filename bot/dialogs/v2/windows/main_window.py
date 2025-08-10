from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from bot.dialogs.v2.states import Wiki, Creation


class MainWindow(Window):
    def __init__(self):
        super().__init__(  # При необходимости, съесть суп вилкой и добавить параметры
                         Const("Добро пожаловаться вам. Служить великий Китай😡"),
                         Button(Const('Категории'), '1', on_click=self.go_to_categories),
                         Button(Const('Страницы'), '2', on_click=self.go_to_pages),
                         Button(Const('Поиск'), '3', on_click=self.go_to_search),
                         Button(Const('Создать'), '4'),
                         state=Wiki.main, )

    async def go_to_categories(self, callback, button, dialog_manager):
        await dialog_manager.switch_to(Wiki.category)

    async def go_to_pages(self, callback, button, dialog_manager):
        await dialog_manager.switch_to(Wiki.category)

    async def go_to_search(self, callback, button, dialog_manager):
        await dialog_manager.switch_to(Wiki.search)


main_window = MainWindow()
