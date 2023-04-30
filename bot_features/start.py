from telegram import InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from bot_features.menu import MENU_INLINE_KEYBOARD
from database.queries.queries import BotUserQuery


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Starts bot for user.
    :return: None
    """
    BotUserQuery(update.effective_user.id).register().close()
    await update.message.reply_html(
        rf"Привет, {update.effective_user.mention_html()}! ",
        reply_markup=InlineKeyboardMarkup(MENU_INLINE_KEYBOARD)
    )
