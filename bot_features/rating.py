from telegram import (InlineQueryResultArticle,
                      InputTextMessageContent,
                      Update,
                      )
from telegram.ext import ContextTypes
from database.queries.queries import BotUserQuery


async def send_rating_from(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Rating from inline query. Sends list of ratings.
    :return: None
    """
    results = []
    for i in range(11):
        results.append(
            InlineQueryResultArticle(id=str(i),
                                     title=str(i),
                                     input_message_content=InputTextMessageContent(
                                         f"/set_rating_from {i}"
                                     ))
        )
    await update.inline_query.answer(results, cache_time=0)


async def set_rating_from(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Sets Filter.rating_from column for particular user.
    :return: None
    """
    await update.message.delete()
    arg = "".join(context.args)
    try:
        arg = int(arg)
        if not 0 <= arg <= 10:
            raise ValueError
    except ValueError:
        return
    query = BotUserQuery(update.effective_user.id).register()
    search_filter = query.filter
    search_filter.rating_from = arg
    query.commit().close()
    await update.message.reply_text(f"Установлен рейтинг от {arg}.")


async def send_rating_to(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Rating to inline query. Sends list of ratings.
    :return: None
    """
    results = []
    for i in range(11):
        results.append(
            InlineQueryResultArticle(id=str(i),
                                     title=str(i),
                                     input_message_content=InputTextMessageContent(
                                         f"/set_rating_to {i}"
                                     ))
        )
    await update.inline_query.answer(results, cache_time=0)


async def set_rating_to(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Sets Filter.rating_to column for particular user.
    :return: None
    """
    await update.message.delete()
    arg = "".join(context.args)
    try:
        arg = int(arg)
        if not 0 <= arg <= 10:
            raise ValueError
    except ValueError:
        return
    query = BotUserQuery(update.effective_user.id).register()
    search_filter = query.filter
    search_filter.rating_to = arg
    query.commit().close()
    await update.message.reply_text(f"Установлен рейтинг до {arg}.")
