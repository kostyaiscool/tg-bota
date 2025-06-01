from aiogram_dialog import Dialog

from bot.dialogs.views import main_window, page_window

# dialog = Dialog(main_window)
# Створюємо діалог, який включає обидва вікна
wiki_dialog = Dialog(
    main_window,  # Вікно з категоріями
    page_window,  # Вікно зі статтями
)
# def setup_dialogs():
#     return [
#         Dialog(
#             main_window,
#             page_window,
#         )
#     ]