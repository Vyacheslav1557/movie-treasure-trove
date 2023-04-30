from kinopoisk_unofficial.model.dictonary.film_type import FilmType

TYPES_IN_RUSSIAN = {
    FilmType.FILM: "фильм",
    FilmType.VIDEO: "видео",
    FilmType.TV_SERIES: "сериал",
    FilmType.MINI_SERIES: "мини-сериал",
    FilmType.TV_SHOW: "телешоу",
    "ALL": "все",
    "FILM": "фильм",
    "VIDEO": "видео",
    "TV_SERIES": "сериал",
    "MINI_SERIES": "мини-сериал",
    "TV_SHOW": "телешоу",
}

TYPES = {
    "все": "ALL",
    "фильм": "FILM",
    "телешоу": "TV_SHOW",
    "сериал": "TV_SERIES",
    "мини-сериал": "MINI_SERIES",
}

FROM_TYPES = {
    "FILM": FilmType.FILM,
    "TV_SHOW": FilmType.TV_SHOW,
    "TV_SERIES": FilmType.TV_SERIES,
    "MINI_SERIES": FilmType.MINI_SERIES,
}


def get_title(item) -> str:
    title = item.name_ru or item.name_en or item.name_original
    if item.name_ru and item.name_en:
        title = f"{item.name_ru} ({item.name_en})"
    return title


def get_short_info(item) -> dict:
    description = {}
    if hasattr(item, "type") and item.type and item.type != "null":
        description["Тип: "] = TYPES_IN_RUSSIAN[item.type]
    if hasattr(item, "year") and item.year and item.year != "null":
        description["Год: "] = str(item.year)

    if hasattr(item, "rating_kinopoisk") and item.rating_kinopoisk:
        item.rating_kinopoisk = str(item.rating_kinopoisk)
        if "%" not in item.rating_kinopoisk and item.rating_kinopoisk != "null":
            description["Рейтинг kinopoisk: "] = item.rating_kinopoisk

    if hasattr(item, "rating_imdb") and item.rating_imdb:
        item.rating_imdb = str(item.rating_imdb)
        if "%" not in item.rating_imdb and item.rating_imdb != "null":
            description["Рейтинг IMDb: "] = item.rating_imdb

    if hasattr(item, "rating") and item.rating:
        item.rating = str(item.rating)
        if "%" not in item.rating and item.rating != "null":
            description["Рейтинг: "] = item.rating

    if hasattr(item, "countries") and item.countries:
        description["Страна: "] = ", ".join([country.country for country in item.countries])
    if hasattr(item, "genres") and item.genres:
        description["Жанр: "] = ", ".join([genre.genre for genre in item.genres])
    return description
