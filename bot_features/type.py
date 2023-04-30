from telegram import (InlineQueryResultArticle,
                      InputTextMessageContent,
                      Update,
                      )
from telegram.ext import ContextTypes
from database.queries.queries import BotUserQuery
from shortcuts.shortcuts import TYPES, TYPES_IN_RUSSIAN


async def send_types(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Types inline query. Sends list of types.
    :return: None
    """
    results = []
    for key, value in TYPES.items():
        results.append(
            InlineQueryResultArticle(id=str(value),
                                     title=key,
                                     input_message_content=InputTextMessageContent(
                                         f"/type {key}"
                                     ))
        )
    await update.inline_query.answer(results)


async def change_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Changes Filter.type for particular user.
    :return: None
    """
    await update.message.delete()
    arg = "".join(context.args)
    if arg not in TYPES:
        await update.message.reply_text("Не удалось найти данный тип. Попробуйте изменить его название.")
        return
    query = BotUserQuery(update.effective_user.id).register()
    search_filter = query.filter
    old_type = TYPES_IN_RUSSIAN[search_filter.type]
    search_filter.type = TYPES[arg]
    new_type = TYPES_IN_RUSSIAN[search_filter.type]
    query.commit().close()
    await update.message.reply_text(f"Тип изменён с {old_type} на {new_type}.")
