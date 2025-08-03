from aiogram_dialog import Dialog

from bot.dialogs.v2.windows.main_window import main_window
from bot.dialogs.v2.windows.page_window import page_window, page_text_window, page_search_window
from bot.dialogs.v2.windows.category_window import category_window, cat_page_window

dialog = Dialog(main_window, page_window, page_text_window, category_window, cat_page_window)
dialog1 = Dialog(page_search_window)