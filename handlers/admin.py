import logging
from telegram import Update
from telegram.ext import ContextTypes

from database import db
from config import ADMIN_IDS
from utils.keyboards import (
    get_admin_keyboard,
    get_order_management_keyboard,
)
from utils.messages import get_orders_message

logger = logging.getLogger(__name__)


def _check_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _check_admin(update.effective_user.id):
        return
    await update.message.reply_text(
        "Панель администратора",
        reply_markup=get_admin_keyboard(),
    )


async def admin_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not _check_admin(update.effective_user.id):
        await query.answer("Нет доступа", show_alert=True)
        return
    await query.answer()
    orders = db.get_all_orders()
    text = get_orders_message([
        (
            o[0], o[2], o[3], o[4], o[5], o[6], o[7], o[8], o[9], o[10]
        )
        for o in orders
    ])
    await query.edit_message_text(text, parse_mode='Markdown')


async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not _check_admin(update.effective_user.id):
        await query.answer("Нет доступа", show_alert=True)
        return
    await query.answer()
    orders = db.get_all_orders()
    total = len(orders)
    paid = sum(1 for o in orders if o[7] == 'paid')
    shipped = sum(1 for o in orders if o[6] == 'shipped')
    text = (
        f"Всего заказов: {total}\n"
        f"Оплачено: {paid}\n"
        f"Отправлено: {shipped}"
    )
    await query.edit_message_text(text)


async def manage_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        cmd = update.message.text
        order_id = int(cmd.split('_')[1])
        order = db.get_order(order_id)
        if not order:
            await update.message.reply_text("Заказ не найден")
            return
        text = get_orders_message([(order[0], order[2], order[3], order[4], order[5], order[6], order[7], order[8], order[9], order[10])])
        await update.message.reply_text(
            text,
            parse_mode='Markdown',
            reply_markup=get_order_management_keyboard(order_id),
        )


async def confirm_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    order_id = int(query.data.split('_')[2])
    db.update_order_status(order_id, 'confirmed', payment_status='paid')
    await query.edit_message_reply_markup(reply_markup=get_order_management_keyboard(order_id))


async def mark_shipped(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    order_id = int(query.data.split('_')[2])
    db.update_order_status(order_id, 'shipped')
    await query.edit_message_reply_markup(reply_markup=get_order_management_keyboard(order_id))


async def mark_delivered(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    order_id = int(query.data.split('_')[2])
    db.update_order_status(order_id, 'delivered')
    await query.edit_message_reply_markup(reply_markup=get_order_management_keyboard(order_id))


async def cancel_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    order_id = int(query.data.split('_')[2])
    db.update_order_status(order_id, 'cancelled', payment_status='refunded')
    await query.edit_message_reply_markup(reply_markup=get_order_management_keyboard(order_id))


async def send_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    order_id = int(query.data.split('_')[2])
    order = db.get_order(order_id)
    if order and order[8]:
        try:
            await context.bot.send_message(order[1], f"Ссылка для отслеживания: {order[8]}")
        except Exception:
            logger.exception("Failed to send link")
    await query.edit_message_reply_markup(reply_markup=get_order_management_keyboard(order_id))

