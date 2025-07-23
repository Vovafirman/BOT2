import logging
from aiogram import types

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


async def admin_panel(message: types.Message):
    if not _check_admin(message.from_user.id):
        return
    await message.answer(
        "Панель администратора",
        reply_markup=get_admin_keyboard(),
    )


async def admin_orders(callback_query: types.CallbackQuery):
    if not _check_admin(callback_query.from_user.id):
        await callback_query.answer("Нет доступа", show_alert=True)
        return
    await callback_query.answer()
    orders = db.get_all_orders()
    text = get_orders_message([
        (
            o[0], o[2], o[3], o[4], o[5], o[6], o[7], o[8], o[9], o[10]
        )
        for o in orders
    ])
    await callback_query.message.edit_text(text, parse_mode='Markdown')


async def admin_stats(callback_query: types.CallbackQuery):
    if not _check_admin(callback_query.from_user.id):
        await callback_query.answer("Нет доступа", show_alert=True)
        return
    await callback_query.answer()
    orders = db.get_all_orders()
    total = len(orders)
    paid = sum(1 for o in orders if o[7] == 'paid')
    shipped = sum(1 for o in orders if o[6] == 'shipped')
    text = (
        f"Всего заказов: {total}\n"
        f"Оплачено: {paid}\n"
        f"Отправлено: {shipped}"
    )
    await callback_query.message.edit_text(text)


async def manage_order(message: types.Message):
    if message.text:
        cmd = message.text
        order_id = int(cmd.split('_')[1])
        order = db.get_order(order_id)
        if not order:
            await message.answer("Заказ не найден")
            return
        text = get_orders_message([(order[0], order[2], order[3], order[4], order[5], order[6], order[7], order[8], order[9], order[10])])
        await message.answer(
            text,
            parse_mode='Markdown',
            reply_markup=get_order_management_keyboard(order_id),
        )


async def confirm_payment(callback_query: types.CallbackQuery):
    await callback_query.answer()
    order_id = int(callback_query.data.split('_')[2])
    db.update_order_status(order_id, 'confirmed', payment_status='paid')
    await callback_query.message.edit_reply_markup(reply_markup=get_order_management_keyboard(order_id))


async def mark_shipped(callback_query: types.CallbackQuery):
    await callback_query.answer()
    order_id = int(callback_query.data.split('_')[2])
    db.update_order_status(order_id, 'shipped')
    await callback_query.message.edit_reply_markup(reply_markup=get_order_management_keyboard(order_id))


async def mark_delivered(callback_query: types.CallbackQuery):
    await callback_query.answer()
    order_id = int(callback_query.data.split('_')[2])
    db.update_order_status(order_id, 'delivered')
    await callback_query.message.edit_reply_markup(reply_markup=get_order_management_keyboard(order_id))


async def cancel_order(callback_query: types.CallbackQuery):
    await callback_query.answer()
    order_id = int(callback_query.data.split('_')[2])
    db.update_order_status(order_id, 'cancelled', payment_status='refunded')
    await callback_query.message.edit_reply_markup(reply_markup=get_order_management_keyboard(order_id))


async def send_link(callback_query: types.CallbackQuery, bot):
    await callback_query.answer()
    order_id = int(callback_query.data.split('_')[2])
    order = db.get_order(order_id)
    if order and order[8]:
        try:
            await bot.send_message(order[1], f"Ссылка для отслеживания: {order[8]}")
        except Exception:
            logger.exception("Failed to send link")
    await callback_query.message.edit_reply_markup(reply_markup=get_order_management_keyboard(order_id))

