from telegram.ext import (
    Application,
    CallbackQueryHandler,
    InlineQueryHandler,
    CommandHandler
)
from bot_features.search import search
from bot_features.start import start
from bot_features.menu import send_menu
from bot_features.film import send_film, send_random_film
from bot_features.work_with_lists import (
    add_to_liked,
    add_to_disliked,
    add_to_favourite,
    add_to_watch_list,
    send_lists_menu
)
from bot_features.filter import send_filter_menu, send_current_filters
from bot_features.type import change_type
from bot_features.genres import add_genre, remove_genre
from bot_features.countries import add_country, remove_country
from bot_features.rating import set_rating_from, set_rating_to
from bot_features.year import set_year_from, set_year_to
from bot_features.reset import reset
from bot_features.help import send_help
from bot_features.recommendation import recommend
import logging
from database.models import db_session
from constants import BOT_TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


def main() -> None:
    db_session.global_init()

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .arbitrary_callback_data(True)
        .build()
    )

    application.add_handler(InlineQueryHandler(search))

    # Команды пользователя
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", send_menu))
    application.add_handler(CommandHandler("help", send_help))
    application.add_handler(CommandHandler("filter", send_filter_menu))
    application.add_handler(CommandHandler("random", send_random_film))
    application.add_handler(CommandHandler("lists", send_lists_menu))
    application.add_handler(CommandHandler("recommend", recommend))

    # Внутренние команды
    application.add_handler(CommandHandler("id", send_film))
    application.add_handler(CommandHandler("type", change_type))
    application.add_handler(CommandHandler("add_genre", add_genre))
    application.add_handler(CommandHandler("remove_genre", remove_genre))
    application.add_handler(CommandHandler("add_country", add_country))
    application.add_handler(CommandHandler("remove_country", remove_country))
    application.add_handler(CommandHandler("set_rating_from", set_rating_from))
    application.add_handler(CommandHandler("set_rating_to", set_rating_to))
    application.add_handler(CommandHandler("set_year_from", set_year_from))
    application.add_handler(CommandHandler("set_year_to", set_year_to))

    application.add_handler(CallbackQueryHandler(send_random_film, "random"))
    application.add_handler(CallbackQueryHandler(send_menu, "menu"))
    application.add_handler(CallbackQueryHandler(recommend, "recommend"))
    application.add_handler(CallbackQueryHandler(send_filter_menu, "filter"))
    application.add_handler(CallbackQueryHandler(add_to_liked, "liked"))
    application.add_handler(CallbackQueryHandler(add_to_disliked, "disliked"))
    application.add_handler(CallbackQueryHandler(add_to_favourite, "favourite"))
    application.add_handler(CallbackQueryHandler(add_to_watch_list, "wanna_watch"))
    application.add_handler(CallbackQueryHandler(reset, "reset"))
    application.add_handler(CallbackQueryHandler(send_current_filters, "current_filters"))
    application.add_handler(CallbackQueryHandler(send_lists_menu, "lists"))

    application.run_polling()


if __name__ == '__main__':
    main()
