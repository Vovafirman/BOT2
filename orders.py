import logging
from telegram import Update
from telegram.ext import ContextTypes
from database import db
from utils.keyboards import get_orders_keyboard
from utils.messages import get_orders_message

logger = logging.getLogger(__name__)

async def my_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle my orders menu"""
    try:
        query = update.callback_query
        await query.answer()

        user_id = update.effective_user.id
        orders = db.get_user_orders(user_id)

        message = get_orders_message(orders)

        await query.edit_message_text(
            text=message,
            parse_mode='Markdown',
            reply_markup=get_orders_keyboard()
        )

    except Exception as e:
        logger.error(f"Error in my_orders handler: {e}")
        await query.answer("Произошла ошибка. Попробуйте позже.")

def get_orders_message(orders):
    """Get user orders message"""
    if not orders:
        return """
📦 **МОИ ЗАКАЗЫ**

У вас пока нет заказов.

Перейдите в каталог товаров, чтобы сделать первую покупку! 🛍️
"""

    message = "📦 **МОИ ЗАКАЗЫ**\n\n"

    for order in orders:
        order_id, product_key, color, quantity, total_price, status, payment_status, tracking_link, created_at, product_name, delivery_address = order

        status_emoji = {
            'pending': '⏳',
            'confirmed': '✅', 
            'shipped': '📦',
            'delivered': '🎯',
            'cancelled': '❌'
        }.get(status, '❓')

        message += f"""
{status_emoji} **Заказ #{order_id}**
📦 Товар: {product_name}
"""

        if color:
            message += f"🎨 Цвет: {color}\n"

        message += f"""💰 Сумма: {total_price} ₽
📊 Статус: {status}
💳 Оплата: {payment_status}
📅 Дата: {created_at[:10]}
"""

        if tracking_link:
            message += f"🚚 Отслеживание: {tracking_link}\n"

        message += "─────────────────\n"

    return message