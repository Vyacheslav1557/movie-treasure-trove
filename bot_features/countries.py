from telegram import (InlineQueryResultArticle,
                      InputTextMessageContent,
                      Update,
                      )
from telegram.ext import ContextTypes
from database.queries.queries import BotUserQuery
from shortcuts.lost_data import filters_response


async def send_countries(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Countries inline query. Sends list of countries.
    :return: None
    """
    query = BotUserQuery(update.effective_user.id).register()
    country_id = query.filter.country
    results = []
    q = update.inline_query.query[10:]
    for item in filters_response.countries:
        if q.strip() and q.lower().strip() not in item.country.lower():
            continue
        if item.country is not None and item.country.strip() == "":
            continue
        if country_id is None or str(item.id) != country_id:
            title = f"Установить {item.country}"
            cmd = f"/add_country {item.id}"
        else:
            title = f"Удалить {item.country}"
            cmd = f"/remove_country {item.id}"
        results.append(
            InlineQueryResultArticle(
                id=str(item.id),
                title=title,
                input_message_content=InputTextMessageContent(
                    cmd
                )
            )
        )
    query.close()
    await update.inline_query.answer(results[:45], cache_time=0)


async def add_country(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Sets Filter.country column for particular user.
    :return: None
    """
    await update.message.delete()
    arg = "".join(context.args)
    for item in filters_response.countries:
        if str(item.id) == arg:
            break
    else:
        return
    query = BotUserQuery(update.effective_user.id).register()
    search_filter = query.filter
    search_filter.country = str(item.id)
    query.commit().close()
    await update.message.reply_text(f"Для параметра страна установлено значение {item.country}.")


async def remove_country(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Sets Filter.country column to None for particular user.
    :return: None
    """
    await update.message.delete()
    arg = "".join(context.args)
    for item in filters_response.countries:
        if str(item.id) == arg:
            break
    else:
        return
    query = BotUserQuery(update.effective_user.id).register()
    search_filter = query.filter
    search_filter.country = None
    query.commit().close()
    await update.message.reply_text(f"Значение параметра страна очищено.")
