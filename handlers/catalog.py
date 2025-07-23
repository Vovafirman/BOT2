import logging
from aiogram import types

from database import db
from config import PRODUCTS, CATEGORIES, ADMIN_IDS
from utils.keyboards import (
    get_catalog_keyboard,
    get_products_keyboard,
    get_product_colors_keyboard,
    get_product_actions_keyboard,
    get_delivery_request_keyboard,
    get_order_confirmation_keyboard,
    get_payment_keyboard,
)
from utils.messages import (
    get_catalog_message,
    get_product_message,
    get_cart_added_message,
    get_delivery_request_message,
    get_order_confirmation_message,
    get_payment_message,
    get_order_created_message,
    get_admin_new_order_message,
)

logger = logging.getLogger(__name__)

async def catalog(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text(
        get_catalog_message(),
        parse_mode="Markdown",
        reply_markup=get_catalog_keyboard(),
    )

async def show_category(callback_query: types.CallbackQuery):
    await callback_query.answer()
    category = callback_query.data.split('_', 1)[1]
    products = db.get_products_by_category(category)
    text = CATEGORIES.get(category, "")
    await callback_query.message.edit_text(
        text,
        reply_markup=get_products_keyboard(products, category),
    )

async def show_product(callback_query: types.CallbackQuery):
    await callback_query.answer()
    product_key = callback_query.data.split('_', 1)[1]
    product = db.get_product(product_key)
    if not product:
        await callback_query.answer("Товар не найден")
        return
    message = get_product_message(product)
    photo_path = f"images/{product['image']}" if product.get('image') else None
    if photo_path:
        with open(photo_path, 'rb') as photo:
            await callback_query.message.answer_photo(photo, caption=message, parse_mode='Markdown', reply_markup=get_product_colors_keyboard(product_key, product['colors']) if product['colors'] else get_product_actions_keyboard(product_key))
        await callback_query.message.delete()
    else:
        await callback_query.message.edit_text(
            message,
            parse_mode='Markdown',
            reply_markup=get_product_colors_keyboard(product_key, product['colors']) if product['colors'] else get_product_actions_keyboard(product_key),
        )

async def select_color(callback_query: types.CallbackQuery):
    await callback_query.answer()
    _, product_key, color = callback_query.data.split('_', 2)
    product = db.get_product(product_key)
    if not product:
        await callback_query.answer("Товар не найден")
        return
    message = get_product_message(product)
    await callback_query.message.edit_text(
        message,
        parse_mode='Markdown',
        reply_markup=get_product_actions_keyboard(product_key, color),
    )

async def add_to_cart(callback_query: types.CallbackQuery):
    await callback_query.answer()
    _, product_key, color = callback_query.data.split('_', 2)
    color = None if color == 'none' else color
    product = db.get_product(product_key)
    if not product:
        await callback_query.answer("Товар не найден")
        return
    success = db.add_to_cart(callback_query.from_user.id, product_key, color)
    if success:
        await callback_query.answer(get_cart_added_message(product['name'], color), show_alert=True)
    else:
        await callback_query.answer("Не удалось добавить", show_alert=True)

async def buy_now(callback_query: types.CallbackQuery, state: dict):
    await callback_query.answer()
    _, product_key, color = callback_query.data.split('_', 2)
    product = db.get_product(product_key)
    if not product:
        await callback_query.answer("Товар не найден")
        return
    state['purchase'] = {
        'product_key': product_key,
        'color': None if color == 'none' else color,
    }
    message = get_delivery_request_message(product['name'], color if color != 'none' else None)
    await callback_query.message.edit_text(
        message,
        parse_mode='Markdown',
        reply_markup=get_delivery_request_keyboard(product_key, color),
    )

async def back_to_category(callback_query: types.CallbackQuery):
    await callback_query.answer()
    product_key = callback_query.data.split('_', 3)[-1]
    product = db.get_product(product_key)
    if not product:
        await callback_query.answer("Товар не найден")
        return
    products = db.get_products_by_category(product['category'])
    text = CATEGORIES.get(product['category'], '')
    await callback_query.message.edit_text(
        text,
        reply_markup=get_products_keyboard(products, product['category']),
    )

async def handle_delivery_address(message: types.Message, state: dict):
    if 'purchase' not in state:
        return
    data = state['purchase']
    data['delivery_address'] = message.text
    product = db.get_product(data['product_key'])
    msg_text = get_order_confirmation_message(product, data['color'], data['delivery_address'])
    await message.answer(
        msg_text,
        parse_mode='Markdown',
        reply_markup=get_order_confirmation_keyboard(data['product_key'], data['color'] or 'none'),
    )

async def confirm_order(callback_query: types.CallbackQuery, state: dict):
    await callback_query.answer()
    _, product_key, color = callback_query.data.split('_', 2)
    data = state.get('purchase')
    if not data or data['product_key'] != product_key:
        await callback_query.answer("Данные заказа не найдены", show_alert=True)
        return
    delivery = data.get('delivery_address')
    order_id = db.create_order(callback_query.from_user.id, product_key, data['color'], 1, delivery)
    if order_id is None:
        await callback_query.answer("Не удалось создать заказ", show_alert=True)
        return
    product = db.get_product(product_key)
    await callback_query.message.edit_text(
        get_order_created_message(order_id, product['name'], data['color'], product['price']),
        parse_mode='Markdown',
        reply_markup=get_payment_keyboard(order_id),
    )
    # notify admins
    text = get_admin_new_order_message(order_id, callback_query.from_user, product['name'], data['color'], delivery, product['price'])
    for admin_id in ADMIN_IDS:
        try:
            await callback_query.bot.send_message(admin_id, text, parse_mode='Markdown')
        except Exception:
            logger.exception("Failed to notify admin %s", admin_id)
    state.pop('purchase', None)

async def payment_done(callback_query: types.CallbackQuery):
    await callback_query.answer("Мы проверим оплату и свяжемся с вами", show_alert=True)
    order_id = int(callback_query.data.split('_')[2])
    db.update_order_status(order_id, 'pending', payment_status='paid')

