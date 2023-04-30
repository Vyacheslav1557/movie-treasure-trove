from telegram import (InlineKeyboardButton,
                      InlineKeyboardMarkup,
                      Update,
                      InlineQueryResultArticle,
                      InputTextMessageContent
                      )
from telegram.ext import ContextTypes
from database.queries.queries import BotUserQuery
from kinopoisk_unofficial.model.filter_country import FilterCountry
from kinopoisk_unofficial.model.filter_genre import FilterGenre
from kinopoisk_unofficial.request.films.film_search_by_filters_request import FilmSearchByFiltersRequest
from api_client.api_client import api_client
from shortcuts.shortcuts import FROM_TYPES, TYPES_IN_RUSSIAN, get_title, get_short_info
from shortcuts.lost_data import filters_response

FILTER_CONFIG_INLINE_KEYBOARD = [
    [InlineKeyboardButton("Фильтр", callback_data="filter")],
    [InlineKeyboardButton("Меню", callback_data="menu")]
]


async def send_filter_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Sends filter menu.
    :return: None
    """
    query = BotUserQuery(update.effective_user.id).register()
    search_filter = query.filter
    year_from, year_to = search_filter.year_from, search_filter.year_to
    filter_menu_inline_keyboard = [
        [InlineKeyboardButton("Текущие фильтры", callback_data="current_filters")],
        [InlineKeyboardButton("Жанры", switch_inline_query_current_chat="#genres"),
         InlineKeyboardButton("Страны", switch_inline_query_current_chat="#countries")],
        [InlineKeyboardButton("Тип", switch_inline_query_current_chat="#type")],
        [InlineKeyboardButton("Рейтинг от", switch_inline_query_current_chat="#rating_from"),
         InlineKeyboardButton("Рейтинг до", switch_inline_query_current_chat="#rating_to")],
        [InlineKeyboardButton("Год от", switch_inline_query_current_chat=f"#year_from {year_from}"),
         InlineKeyboardButton("Год до", switch_inline_query_current_chat=f"#year_to {year_to}")],
        [InlineKeyboardButton("Сбросить", callback_data="reset")],
        [InlineKeyboardButton("Меню", callback_data="menu")],
        [InlineKeyboardButton("Искать по фильтру", switch_inline_query_current_chat="#filter"),
         InlineKeyboardButton("Рандом", callback_data="random")]
    ]
    if not update.callback_query:
        await update.message.reply_text("Выберите изменяемый параметр:",
                                        reply_markup=InlineKeyboardMarkup(filter_menu_inline_keyboard))
        return
    await update.callback_query.answer()
    await update.callback_query.message.edit_text("Выберите изменяемый параметр:",
                                                  reply_markup=InlineKeyboardMarkup(filter_menu_inline_keyboard))


async def search_with_filter(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Finds films considering Filter config.
    :return: None
    """
    query = BotUserQuery(update.effective_user.id).register()
    search_filter = query.filter
    request = FilmSearchByFiltersRequest()
    if search_filter.country:
        request.countries = [FilterCountry(int(search_filter.country), "")]
    if search_filter.genre:
        request.genres = [FilterGenre(int(search_filter.genre), "")]
    if search_filter.type != "ALL":
        request.type = FROM_TYPES[search_filter.type]
    request.rating_from = search_filter.rating_from
    request.rating_to = search_filter.rating_to
    request.year_from = search_filter.year_from
    request.year_to = search_filter.year_to
    results = []
    try:
        response = api_client.films.send_film_search_by_filters_request(request)
        for item in response.items:
            title = get_title(item)
            results.append(
                InlineQueryResultArticle(
                    id=str(item.kinopoisk_id),
                    title=title,
                    description=" | ".join(get_short_info(item).values()),
                    input_message_content=InputTextMessageContent(
                        f"/id {item.kinopoisk_id}"
                    ),
                    thumbnail_url=item.poster_url_preview
                )
            )
        if not results:
            raise ValueError
    except:
        results.append(
            InlineQueryResultArticle(
                id='0',
                title="Ничего не найдено",
                description="Попробуйте ввести другой запрос или нажмите сюда чтобы смотреть инструкцию",
                input_message_content=InputTextMessageContent("/help")
            )
        )
    query.close()
    await update.inline_query.answer(results, cache_time=0)


async def send_current_filters(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Sends current Filter config.
    :return: None
    """
    await update.callback_query.answer()
    query = BotUserQuery(update.effective_user.id).register()
    search_filter = query.filter
    text = []
    if search_filter.country:
        for item in filters_response.countries:
            if str(item.id) == search_filter.country:
                text.append("Страна: " + item.country)
    else:
        text.append("Страны: все")
    if search_filter.genre:
        for item in filters_response.genres:
            if str(item.id) == search_filter.genre:
                text.append("Жанр: " + item.genre)
    else:
        text.append("Жанры: все")
    text.append("Тип: " + TYPES_IN_RUSSIAN[search_filter.type])
    text.append(f"Рейтинг от: {search_filter.rating_from}")
    text.append(f"Рейтинг до: {search_filter.rating_to}")
    text.append(f"Год от: {search_filter.year_from}")
    text.append(f"Год до: {search_filter.year_to}")
    query.close()
    await update.callback_query.edit_message_text("\n".join(text),
                                                  reply_markup=InlineKeyboardMarkup(FILTER_CONFIG_INLINE_KEYBOARD))
