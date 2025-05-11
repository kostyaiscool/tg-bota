from sqladmin import ModelView

from db.models.categories import Category
from db.models.pages import Page
from db.models.user import User


class UserAdmin(ModelView, model=User):
    column_list = [
        User.id,
        User.username,
        User.first_name,
        User.last_name,
        User.language_code,
        User.is_premium,
        User.is_bot,
        User.created_at,
        User.updated_at,
    ]
    form_columns = [
        User.id,
        User.username,
        User.first_name,
        User.last_name,
        User.language_code,
        User.is_premium,
        User.is_bot,
        User.created_at,
        User.updated_at,
    ]

class PageAdmin(ModelView, model=Page):
    column_list = ['id', 'name', 'text', 'creation_date', 'likes', 'dislikes', 'categories', 'author']
    form_columns = ['name', 'text', 'categories', 'author']

class CategoryAdmin(ModelView, model=Category):
    column_list = ['id', 'name']
    form_columns = ['name']