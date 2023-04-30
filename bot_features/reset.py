from telegram import Update
from telegram.ext import ContextTypes
from database.queries.queries import BotUserQuery


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Sets Filter config to default.
    :return: None
    """
    await update.callback_query.answer()
    query = BotUserQuery(update.effective_user.id).register()
    search_filter = query.filter
    search_filter.country = None
    search_filter.genre = None
    search_filter.type = "ALL"
    search_filter.rating_from = 5
    search_filter.rating_to = 10
    search_filter.year_from = 1000
    search_filter.year_to = 3000
    query.commit().close()
    await context.bot.send_message(update.effective_user.id, f"Настройки фильтра сброшены.")
