from telegram import Update
from telegram.ext import ContextTypes

TEXT = "К сожалению, данная функция временно недоступна."


async def recommend(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.reply_text(TEXT)
        return
    await update.message.reply_text(TEXT)
