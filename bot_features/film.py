from telegram import (InlineKeyboardButton,
                      InlineKeyboardMarkup,
                      Update
                      )
from telegram.ext import ContextTypes
from telegram.constants import MessageLimit, ParseMode
from kinopoisk_unofficial.request.films.film_request import FilmRequest
from kinopoisk_unofficial.client.exception.not_found import NotFound
from kinopoisk_unofficial.model.filter_country import FilterCountry
from kinopoisk_unofficial.model.filter_genre import FilterGenre
from kinopoisk_unofficial.request.films.film_search_by_filters_request import FilmSearchByFiltersRequest
from api_client.api_client import api_client
from shortcuts.shortcuts import get_title, get_short_info, FROM_TYPES
from database.queries.queries import BotUserQuery, BotFilmQuery
from random import randint, choice

FILM_STRINGS = {
    "favourite":
        {
            False: "В избранное",
            True: "Из избранного",
        },
    "liked":
        {
            False: "В понравившиеся",
            True: "Из понравившихся",
        },
    "disliked":
        {
            False: "В непонравившиеся",
            True: "Из непонравившихся",
        },
    "wanna_watch":
        {
            False: "В список ожидания",
            True: "Из списка ожидания"
        }
}


async def send_film(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Sends film by film_id.
    :return: None
    """
    film_id = "".join(context.args)

    if update.message:
        await update.message.delete()
    if update.callback_query and update.callback_query.message:
        await update.callback_query.message.delete()
    try:
        request = FilmRequest(int(film_id))
        item = api_client.films.send_film_request(request).film
    except NotFound:
        await update.message.reply_text(rf"Ничего не найдено. "
                                        rf"Попробуйте ввести другой запрос "
                                        rf"или нажмите сюда чтобы смотреть инструкцию: /help")
        return
    caption = []
    title = get_title(item)
    short_info = get_short_info(item)
    short_info = "\n".join([" ".join(p) for p in short_info.items()])
    if title:
        caption.append(title)
        film_query = BotFilmQuery(int(film_id))
        film_query.film_title = title
        film_query.commit().close()
    if short_info:
        caption.append(short_info)
    if item.description and len(item.description) < MessageLimit.CAPTION_LENGTH - len(title) - len(short_info):
        caption.append(item.description)
    caption = "\n\n".join(caption)
    query = BotUserQuery(update.effective_user.id).register()
    user = query.user
    film_inline_keyboard = []
    for key, value in FILM_STRINGS.items():
        ids = user.__dict__[key]
        film_inline_keyboard.append(
            [InlineKeyboardButton(text=value[film_id in ids.split()],
                                  callback_data=key + " " + film_id)]
        )
    film_inline_keyboard.append([
        InlineKeyboardButton(
            "Рандом",
            callback_data="random"),
        InlineKeyboardButton(
            "Похожие",
            switch_inline_query_current_chat=f"#similar {film_id}")
    ])
    film_inline_keyboard.append([
        InlineKeyboardButton("Меню", callback_data="menu")
    ])
    film_inline_keyboard.append([
        InlineKeyboardButton(
            "Страница фильма",
            url=item.web_url)
    ])
    query.close()
    await context.bot.send_photo(update.effective_chat.id,
                                 item.poster_url_preview,
                                 caption=caption,
                                 reply_markup=InlineKeyboardMarkup(film_inline_keyboard),
                                 parse_mode=ParseMode.HTML
                                 )


async def send_random_film(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Sends random film considering Filter config.
    :return: None
    """
    if update.callback_query:
        await update.callback_query.answer()
    query = BotUserQuery(update.effective_user.id).register()
    search_filter = query.filter
    request = FilmSearchByFiltersRequest()
    if search_filter.country is not None:
        request.countries = [FilterCountry(int(search_filter.country), "")]
    if search_filter.genre is not None:
        request.genres = [FilterGenre(int(search_filter.genre), "")]
    if search_filter.type != "ALL":
        request.type = FROM_TYPES[search_filter.type]
    request.rating_from = search_filter.rating_from
    request.rating_to = search_filter.rating_to
    request.year_from = search_filter.year_from
    request.year_to = search_filter.year_to
    response = api_client.films.send_film_search_by_filters_request(request)
    request.page = randint(1, response.totalPages)
    response = api_client.films.send_film_search_by_filters_request(request)
    query.commit().close()
    try:
        item = choice(response.items)
        film_id = item.kinopoisk_id
    except ValueError:
        await update.message.reply_text(rf"Ничего не найдено. "
                                        rf"Попробуйте ввести другой запрос "
                                        rf"или нажмите сюда чтобы смотреть инструкцию: /help")
        return
    context.args = str(film_id)
    await send_film(update, context)
