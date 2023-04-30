from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import ContextTypes
from kinopoisk_unofficial.request.films.film_top_request import FilmTopRequest
from kinopoisk_unofficial.model.dictonary.top_type import TopType
from kinopoisk_unofficial.request.films.film_search_by_filters_request import FilmSearchByFiltersRequest
from kinopoisk_unofficial.request.films.related_film_request import RelatedFilmRequest
from api_client.api_client import api_client
from shortcuts.shortcuts import get_title, get_short_info
from bot_features.film import FILM_STRINGS
from bot_features.type import send_types
from bot_features.genres import send_genres
from bot_features.countries import send_countries
from bot_features.rating import send_rating_from, send_rating_to
from bot_features.year import send_year_from, send_year_to
from bot_features.filter import search_with_filter
from bot_features.work_with_lists import send_list


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Manages all inline queries.
    :return: None
    """
    query = update.inline_query.query.strip()
    if not query:
        request = FilmTopRequest(TopType.TOP_100_POPULAR_FILMS)
        response = api_client.films.send_film_top_request(request)
        items = response.films
    elif query == "#filter":
        await search_with_filter(update, context)
        return
    elif query.startswith("#similar"):
        items = []
        try:
            film_id = int(query[8:])
            request = RelatedFilmRequest(film_id)
            response = api_client.films.send_related_film_request(request)
            items = response.items
        except:
            pass
    elif query == "#type":
        await send_types(update, context)
        return
    elif query.startswith("#genres"):
        await send_genres(update, context)
        return
    elif query.startswith("#countries"):
        await send_countries(update, context)
        return
    elif query.startswith("#rating_from"):
        await send_rating_from(update, context)
        return
    elif query.startswith("#rating_to"):
        await send_rating_to(update, context)
        return
    elif query.startswith("#year_from"):
        await send_year_from(update, context)
        return
    elif query.startswith("#year_to"):
        await send_year_to(update, context)
        return
    elif any(query == "#" + key for key in FILM_STRINGS):
        await send_list(update, context)
        return
    elif query:
        request = FilmSearchByFiltersRequest()
        request.keyword = query
        response = api_client.films.send_film_search_by_filters_request(request)
        items = response.items
    else:
        return

    results = []
    for item in items:
        title = get_title(item)
        film_id = 0
        if hasattr(item, "film_id"):
            film_id = item.film_id
        elif hasattr(item, "kinopoisk_id"):
            film_id = item.kinopoisk_id
        results.append(
            InlineQueryResultArticle(
                id=str(film_id),
                title=title,
                description=" | ".join(get_short_info(item).values()),
                input_message_content=InputTextMessageContent(
                    f"/id {film_id}"
                ),
                thumbnail_url=item.poster_url_preview
            )
        )
    if not results:
        results.append(
            InlineQueryResultArticle(
                id='0',
                title="Ничего не найдено",
                description="Попробуйте ввести другой запрос или нажмите сюда чтобы смотреть инструкцию",
                input_message_content=InputTextMessageContent("/help")
            )
        )
    await update.inline_query.answer(results, cache_time=3)
