from telegram import (InlineQueryResultArticle,
                      InputTextMessageContent,
                      Update,
                      )
from telegram.ext import ContextTypes
from database.queries.queries import BotUserQuery
from shortcuts.lost_data import filters_response


async def send_genres(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Genres inline query. Sends list of genres.
    :return: None
    """
    query = BotUserQuery(update.effective_user.id).register()
    search_filter = query.filter
    genre_id = search_filter.genre
    results = []
    q = update.inline_query.query[8:]
    for item in filters_response.genres:
        if q.strip() and q.lower().strip() not in item.genre.lower():
            continue
        if item.genre is not None and item.genre.strip() == "":
            continue
        if genre_id is None or str(item.id) != genre_id:
            title = f"Установить {item.genre}"
            cmd = f"/add_genre {item.id}"
        else:
            title = f"Удалить {item.genre}"
            cmd = f"/remove_genre {item.id}"
        results.append(
            InlineQueryResultArticle(id=str(item.id),
                                     title=title,
                                     input_message_content=InputTextMessageContent(
                                         cmd
                                     ))
        )
    query.commit().close()
    await update.inline_query.answer(results, cache_time=0)


async def add_genre(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Sets Filter.genre column for particular user.
    :return: None
    """
    await update.message.delete()
    arg = "".join(context.args)
    for item in filters_response.genres:
        if str(item.id) == arg:
            break
    else:
        return
    query = BotUserQuery(update.effective_user.id).register()
    search_filter = query.filter
    search_filter.genre = str(item.id)
    query.commit().close()
    await update.message.reply_text(f"Для параметра жанр установлено значение {item.genre}.")


async def remove_genre(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Sets Filter.genre column to None for particular user.
    :return: None
    """
    await update.message.delete()
    arg = "".join(context.args)
    for item in filters_response.genres:
        if str(item.id) == arg:
            break
    else:
        return
    query = BotUserQuery(update.effective_user.id).register()
    search_filter = query.filter
    search_filter.genre = None
    query.commit().close()
    await update.message.reply_text(f"Значение параметра жанр очищено.")
