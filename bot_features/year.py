from telegram import (InlineQueryResultArticle,
                      InputTextMessageContent,
                      Update,
                      )
from telegram.ext import ContextTypes
from database.queries.queries import BotUserQuery


async def send_year_from(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Year from inline query. Sends year if value is correct.
    :return: None
    """
    q = update.inline_query.query[10:]
    try:
        q = int(q)
        if not 1000 <= q <= 3000:
            raise ValueError
    except ValueError:
        return
    results = [InlineQueryResultArticle(id=str(0),
                                        title=str(q),
                                        input_message_content=InputTextMessageContent(
                                            f"/set_year_from {q}"
                                        ))
               ]
    await update.inline_query.answer(results, cache_time=0)


async def set_year_from(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Sets Filter.year_from column for particular user.
    :return: None
    """
    await update.message.delete()
    arg = "".join(context.args)
    try:
        arg = int(arg)
        if not 1000 <= arg <= 3000:
            raise ValueError
    except ValueError:
        return
    query = BotUserQuery(update.effective_user.id).register()
    search_filter = query.filter
    search_filter.year_from = arg
    query.commit().close()
    await update.message.reply_text(f"Установлен год от {arg}.")


async def send_year_to(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Year to inline query. Sends year if value is correct.
    :return: None
    """
    q = update.inline_query.query[9:]
    try:
        q = int(q)
        if not 1000 <= q <= 3000:
            raise ValueError
    except ValueError:
        return
    results = [InlineQueryResultArticle(id=str(0),
                                        title=str(q),
                                        input_message_content=InputTextMessageContent(
                                            f"/set_year_to {q}"
                                        ))
               ]
    await update.inline_query.answer(results, cache_time=0)


async def set_year_to(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Sets Filter.year_to column for particular user.
    :return: None
    """
    await update.message.delete()
    arg = "".join(context.args)
    try:
        arg = int(arg)
        if not 1000 <= arg <= 3000:
            raise ValueError
    except ValueError:
        return
    query = BotUserQuery(update.effective_user.id).register()
    search_filter = query.filter
    search_filter.year_to = arg
    query.commit().close()
    await update.message.reply_text(f"Установлен год до {arg}.")
