from telegram import (InlineKeyboardButton,
                      InlineKeyboardMarkup,
                      Update,
                      InlineQueryResultArticle,
                      InputTextMessageContent
                      )
from telegram.ext import ContextTypes
from kinopoisk_unofficial.request.films.film_request import FilmRequest
from database.queries.queries import BotUserQuery, BotFilmQuery
from api_client.api_client import api_client
from shortcuts.shortcuts import get_title
from bot_features.menu import send_menu

LIST_MENU_INLINE_KEYBOARD = [
    [InlineKeyboardButton("Избранное", switch_inline_query_current_chat="#favourite")],
    [InlineKeyboardButton("Понравившиеся", switch_inline_query_current_chat="#liked")],
    [InlineKeyboardButton("Непонравившиеся", switch_inline_query_current_chat="#disliked")],
    [InlineKeyboardButton("Список ожидания", switch_inline_query_current_chat="#wanna_watch")],
    [InlineKeyboardButton("Меню", callback_data="menu")]
]


async def final_stage(update: Update, context: ContextTypes.DEFAULT_TYPE,
                      film_id: int, caption: str) -> None:
    """
    Shortcut for work-with-list functions.
    :return: None
    """
    request = FilmRequest(film_id)
    item = api_client.films.send_film_request(request).film
    title = get_title(item)
    if update.callback_query:
        await context.bot.edit_message_caption(chat_id=update.callback_query.message.chat_id,
                                               message_id=update.callback_query.message.message_id,
                                               caption=f"{title} {caption}")
    else:
        await update.message.reply_text(f"{title} {caption}")
    await send_menu(update, context)


async def add_to_favourite(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Changes User.favourite.
    :return: None
    """
    await update.callback_query.answer()
    query = BotUserQuery(update.effective_user.id).register()
    film_id = update.callback_query.data.split()[1]
    user = query.user
    if film_id not in user.favourite.split():
        user.favourite = " ".join(set(user.favourite.split()) | {film_id})
        msg_text = "добавлен в избранное."
    else:
        user.favourite = " ".join(set(user.favourite.split()) - {film_id})
        msg_text = "удален из избранного."
    query.commit().close()
    await final_stage(update, context, int(film_id), msg_text)


async def add_to_liked(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Changes User.liked.
    :return: None
    """
    await update.callback_query.answer()
    query = BotUserQuery(update.effective_user.id).register()
    film_id = update.callback_query.data.split()[1]
    user = query.user
    if film_id not in user.liked.split():
        user.liked = " ".join(set(user.liked.split()) | {film_id})
        user.disliked = " ".join(set(user.disliked.split()) - {film_id})
        msg_text = "добавлен в понравившиеся."
    else:
        user.liked = " ".join(set(user.liked.split()) - {film_id})
        msg_text = "удален из понравившихся."
    query.commit().close()
    await final_stage(update, context, int(film_id), msg_text)


async def add_to_disliked(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Changes User.disliked.
    :return: None
    """
    await update.callback_query.answer()
    query = BotUserQuery(update.effective_user.id).register()
    film_id = update.callback_query.data.split()[1]
    user = query.user
    if film_id not in user.disliked.split():
        user.liked = " ".join(set(user.liked.split()) - {film_id})
        user.disliked = " ".join(set(user.disliked.split()) | {film_id})
        msg_text = "добавлен в непонравившиеся."
    else:
        user.disliked = " ".join(set(user.disliked.split()) - {film_id})
        msg_text = "удален из непонравившихся."
    query.commit().close()
    await final_stage(update, context, int(film_id), msg_text)


async def add_to_watch_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Changes User.wanna_watch.
    :return: None
    """
    await update.callback_query.answer()
    query = BotUserQuery(update.effective_user.id).register()
    film_id = update.callback_query.data.split()[1]
    user = query.user
    if film_id not in user.wanna_watch.split():
        user.wanna_watch = " ".join(set(user.wanna_watch.split()) | {film_id})
        msg_text = "добавлен в список ожидания просмотра."
    else:
        user.wanna_watch = " ".join(set(user.wanna_watch.split()) - {film_id})
        msg_text = "удален из списка ожидания просмотра."
    query.commit().close()
    await final_stage(update, context, int(film_id), msg_text)


async def send_lists_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Sends list menu.
    :return: None
    """
    if not update.callback_query:
        await update.message.reply_text(
            "Выберите список, который хотите просмотреть.",
            reply_markup=InlineKeyboardMarkup(LIST_MENU_INLINE_KEYBOARD))
        return
    await update.callback_query.answer()
    await update.callback_query.message.edit_text(
        "Выберите список, который хотите просмотреть.",
        reply_markup=InlineKeyboardMarkup(LIST_MENU_INLINE_KEYBOARD))


async def send_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    List inline query. Sends chosen list.
    :return: None
    """
    if update.callback_query:
        await update.callback_query.answer()
    query = BotUserQuery(update.effective_user.id).register()
    inline_query = update.inline_query.query.strip()[1:]
    results = []
    for film_id in query.user.__dict__[inline_query].split():
        film_query = BotFilmQuery(int(film_id))
        results.append(
            InlineQueryResultArticle(
                id=film_id,
                title=film_query.film_title.title,
                input_message_content=InputTextMessageContent(
                    f"/id {film_id}"
                )
            )
        )
        film_query.commit().close()
    query.close()
    if not results:
        results.append(
            InlineQueryResultArticle(
                id='0',
                title=f"Список {inline_query} пустой.",
                description="Добавьте данные в этот список, чтобы они отобразились здесь.",
                input_message_content=InputTextMessageContent("/help")
            )
        )
    await update.inline_query.answer(results, cache_time=0)
