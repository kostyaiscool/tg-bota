from functools import wraps
from typing import Callable
from aiogram.types import CallbackQuery, Message
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import db_helper
from db.crud.user import TelegramUserCRUD


def require_permission(permission: str):
    """
    Декоратор для перевірки прав доступу.

    Usage:
        @require_permission("manage_products")
        async def on_create_product(...):
            ...
    """

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user = None
            dialog_manager = None

            for arg in args:
                if isinstance(arg, (CallbackQuery, Message)):
                    if hasattr(arg, 'from_user'):
                        user = kwargs.get('user')
                        break

            if 'dialog_manager' in kwargs:
                dialog_manager = kwargs['dialog_manager']
                user = dialog_manager.middleware_data.get('user')

            if not user:
                return await func(*args, **kwargs)

            # Перевіряємо права
            if not user.has_permission(permission):
                # Відправляємо повідомлення про відсутність доступу
                for arg in args:
                    if isinstance(arg, CallbackQuery):
                        await arg.answer("❌ У вас немає доступу до цієї функції.", show_alert=True)
                        return
                    elif isinstance(arg, Message):
                        await arg.answer("❌ У вас немає доступу до цієї функції.")
                        return

                return

            return await func(*args, **kwargs)

        return wrapper

    return decorator


# def require_role(role: str):
#     """
#     Декоратор для перевірки ролі.
#
#     Usage:
#         @require_role("admin")
#         async def on_admin_panel(...):
#             ...
#     """
#
#     def decorator(func: Callable):
#         global result
#         @wraps(func)
#         async def wrapper(*args, **kwargs):
#             user = None
#             dialog_manager = None
#             print("243238032308")
#             for arg in args:
#                 print(arg)
#                 print("**********************************************************")
#             print(type(args[1]))
#             user_id = args[1].from_user.id
#             async with db_helper.session() as session:
#                 result = await TelegramUserCRUD.has_role(session, role, user_id)
#             print(result)
#             return await func(*args, **kwargs)
#
#         return wrapper
#
#     return decorator

def require_role(roles: list):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            callback = args[1]  # да, пока так
            user_id = callback.from_user.id

            async with db_helper.session() as session:
                for role in roles:
                    has_role = await TelegramUserCRUD.has_role(
                        session, role, user_id
                    )
                    if has_role:
                        break
                else:
                    await callback.answer("❌ У вас нет прав", show_alert=True)
                    return

            return await func(*args, **kwargs)

        return wrapper
    return decorator
