from aiogram.utils.formatting import Bold
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Select, ScrollingGroup, Button
from aiogram_dialog.widgets.text import Format, Const

from bot.dialogs.v2.states import Wiki
from db import db_helper
from db.crud.commentaries import CommentCRUD
from db.crud.pages import PageCRUD

class AllCommentsWindow(Window):
    def __init__(self):
        self.comment_select = Select(
            Format("{item[0]}"),  # отображаемое имя
            id="comment_select",
            item_id_getter=lambda item: item[1],  # page.id
            items="comments",  # ключ из getter'а
            on_click=self.choose_comment,
        )
        self.comment_scrolling = ScrollingGroup(
            self.comment_select,
            id="comments",
            width=1,
            height=6,
        )
        super().__init__(
            Const('t'),
            Button(Const('Назад'), '2', on_click=self.go_to_pages),
            self.comment_scrolling,
            getter=self.comment_getter,
            state=Wiki.comments
        )

    async def comment_getter(self, dialog_manager: DialogManager, **kwargs):
        page_id = dialog_manager.dialog_data.get("page_id", "")
        async with db_helper.session() as session:
            comments = await CommentCRUD.get_page_comments(session, int(page_id))
            print("eeeeee", comments)
        return {
            "comments": [(comment.text, str(comment.id)) for comment in comments]
        }

    async def choose_comment(self, callback, button, dialog_manager: DialogManager, item_id: str):
        print(int(item_id), "В луа, если добавить 2 как строку и 2 как строку, будет 4. Это не тупость, просто для...")
        # pass
        dialog_manager.dialog_data["comment_id"] = int(item_id)
        await dialog_manager.switch_to(Wiki.comment_page)

    async def go_to_pages(self, callback, button, dialog_manager: DialogManager):
        await dialog_manager.switch_to(Wiki.page)

class CommentWindow(Window):
    def __init__(self):
        self.comment_select = Select(
            Format("{item[0]}"),
            id="comment_select",
            item_id_getter=lambda item: item[1],
            items="comments",
            on_click=self.choose_comments,
        )
        self.replies = ScrollingGroup(
            Select(
                Format("↳ {item.text}"),
                id="reply_select",
                item_id_getter=lambda c: c.id,
                items="replies",
                on_click=self.open_reply
            ),
            id="replies",
            width=1,
            height=5,
        )
        super().__init__(
            Bold(Format("{comment.text}")),

            Const("\n💬 Ответы:\n"),

            self.replies,

            Button(Const("✍️ Ответить"), "reply", on_click=self.go_to_reply),
            Button(Const("Назад"), "back", on_click=self.go_to_comments),

            getter=self.comment_getter,
            state=Wiki.comment_page,
        )

    async def choose_comments(self, callback, button, dialog_manager: DialogManager, item_id: str):
        dialog_manager.dialog_data["comment_id"] = int(item_id)
        await dialog_manager.switch_to(Wiki.page_text)

    async def comment_getter(self, dialog_manager: DialogManager, **kwargs):
        comment_id = dialog_manager.dialog_data.get("comment_id")

        async with db_helper.session() as session:
            comment = await CommentCRUD.get_comment_with_replies(session, comment_id)

        return {
            "comment": comment,
            "replies": comment.children
        }

    async def go_to_comments(self, callback, button, dialog_manager: DialogManager):
        await dialog_manager.switch_to(Wiki.comments)


    async def go_back(self, callback, button, dialog_manager: DialogManager):
        # dialog_manager.dialog_data["page_id"] = int(item_id)
        await dialog_manager.switch_to(Wiki.comments)

    async def go_to_reply(self, callback, button, dialog_manager: DialogManager):
        # dialog_manager.dialog_data["page_id"] = int(item_id)
        await dialog_manager.switch_to(Wiki.reply)


comments_window = AllCommentsWindow()
comment_window = CommentWindow()