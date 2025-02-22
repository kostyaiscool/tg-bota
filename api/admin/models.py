from sqladmin import ModelView

from db.models.user import TelegramUser


class UserAdmin(ModelView, model=TelegramUser):
    column_list = [
        TelegramUser.id,
        TelegramUser.username,
        TelegramUser.first_name,
        TelegramUser.last_name,
        TelegramUser.language_code,
        TelegramUser.is_premium,
        TelegramUser.is_bot,
        TelegramUser.created_at,
        TelegramUser.updated_at,
    ]
    form_columns = [
        TelegramUser.id,
        TelegramUser.username,
        TelegramUser.first_name,
        TelegramUser.last_name,
        TelegramUser.language_code,
        TelegramUser.is_premium,
        TelegramUser.is_bot,
        TelegramUser.created_at,
        TelegramUser.updated_at,
    ]
