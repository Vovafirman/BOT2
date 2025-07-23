import logging
from telegram import Update
from telegram.ext import ContextTypes

from database import db
from utils.keyboards import get_orders_keyboard
from utils.messages import get_orders_message

logger = logging.getLogger(__name__)

async def my_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        await query.answer()
        user_id = update.effective_user.id
        orders = db.get_user_orders(user_id)
        await query.edit_message_text(
            get_orders_message(orders),
            parse_mode='Markdown',
            reply_markup=get_orders_keyboard(),
        )
    except Exception as e:
        logger.exception("my_orders failed: %s", e)
        if update.callback_query:
            await update.callback_query.answer("Ошибка")

