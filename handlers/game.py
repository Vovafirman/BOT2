from telegram import Update
from telegram.ext import ContextTypes

from utils.keyboards import get_game_keyboard
from utils.messages import get_game_message

async def game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        get_game_message(),
        parse_mode='Markdown',
        reply_markup=get_game_keyboard(),
    )

