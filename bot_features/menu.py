from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import ContextTypes
from telegram.error import BadRequest
from database.queries.queries import BotUserQuery
from datetime import datetime

MENU_INLINE_KEYBOARD = [
    [InlineKeyboardButton("Рандом", callback_data="random"),
     InlineKeyboardButton("Фильтр", callback_data="filter")],
    [InlineKeyboardButton("Начать поиск", switch_inline_query_current_chat="")],
    [InlineKeyboardButton("Начать подбор (beta)", callback_data="recommend")],
    [InlineKeyboardButton("Списки", callback_data="lists")],
    [InlineKeyboardButton("Автор", url="https://t.me/Vyacheslav1557")]

]


async def send_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Sends menu.
    :return: None
    """
    query = BotUserQuery(update.effective_user.id).register()
    registration_datetime: datetime = query.user.registered_datetime
    text = (f"Дата регистрации: {registration_datetime.strftime('%Y-%m-%d %H:%M')}\n"
            f"Приятного просмотра!")
    query = update.callback_query
    if not query:
        await update.message.reply_text(text,
                                        reply_markup=InlineKeyboardMarkup(MENU_INLINE_KEYBOARD))
        return
    try:
        await query.answer()
        await query.message.edit_text(text,
                                      reply_markup=InlineKeyboardMarkup(MENU_INLINE_KEYBOARD))
    except BadRequest:
        await context.bot.send_message(update.effective_user.id, text,
                                       reply_markup=InlineKeyboardMarkup(MENU_INLINE_KEYBOARD))
