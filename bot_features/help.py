from telegram import Update
from telegram.ext import ContextTypes

HELP = ("/menu - Меню\n"
        "/help - Помощь\n"
        "/filter - Меню фильтра\n"
        "/random - Случайный фильм с учётом фильтров\n"
        "/lists - Открыть меню списков\n"
        "/recommend - Начать подбор\n")


async def send_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Sends help message.
    :return: None
    """
    await update.message.reply_text(HELP)
