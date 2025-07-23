import logging
from aiogram import types

from database import db
from utils.keyboards import get_orders_keyboard
from utils.messages import get_orders_message

logger = logging.getLogger(__name__)

async def my_orders(callback_query: types.CallbackQuery):
    try:
        await callback_query.answer()
        user_id = callback_query.from_user.id
        orders = db.get_user_orders(user_id)
        await callback_query.message.edit_text(
            get_orders_message(orders),
            parse_mode='Markdown',
            reply_markup=get_orders_keyboard(),
        )
    except Exception as e:
        logger.exception("my_orders failed: %s", e)
        await callback_query.answer("Ошибка", show_alert=True)

