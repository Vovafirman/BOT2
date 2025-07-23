import logging
from collections import defaultdict

import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, Text, Regexp

from config import BOT_TOKEN, SUPPORT_USERNAME
from handlers import (
    start, open_store, main_menu,
    catalog, show_category, show_product, select_color,
    add_to_cart, buy_now, back_to_category, handle_delivery_address,
    confirm_order, payment_done,
    my_orders, game,
    admin_panel, admin_orders, admin_stats, manage_order,
    confirm_payment, mark_shipped, mark_delivered, cancel_order,
    send_link,
)
from utils.keyboards import get_back_to_main_keyboard


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Simple per-user state storage
user_states = defaultdict(dict)


@dp.callback_query(Text('help'))
async def help_handler(callback_query: types.CallbackQuery):
    await callback_query.answer()
    message = (
        "❓ **ПОМОЩЬ**\n\n"
        "Для получения помощи обратитесь к нашему оператору:\n\n"
        f"👤 {SUPPORT_USERNAME}"
    )
    await callback_query.message.edit_text(message, parse_mode='Markdown', reply_markup=get_back_to_main_keyboard())


@dp.message(Command('start'))
async def handle_start(message: types.Message):
    await start(message)


@dp.message(Command('admin'))
async def handle_admin(message: types.Message):
    await admin_panel(message)


@dp.message(Regexp(r'^/manage_\d+$'))
async def handle_manage(message: types.Message):
    await manage_order(message)


@dp.callback_query(Text('open_store'))
async def handle_open_store(callback_query: types.CallbackQuery):
    await open_store(callback_query)


@dp.callback_query(Text('main_menu'))
async def handle_main_menu(callback_query: types.CallbackQuery):
    await main_menu(callback_query)


@dp.callback_query(Text('catalog'))
async def handle_catalog(callback_query: types.CallbackQuery):
    await catalog(callback_query)


@dp.callback_query(Text(startswith='category_'))
async def handle_show_category(callback_query: types.CallbackQuery):
    await show_category(callback_query)


@dp.callback_query(Text(startswith='product_'))
async def handle_show_product(callback_query: types.CallbackQuery):
    await show_product(callback_query)


@dp.callback_query(Text(startswith='color_'))
async def handle_select_color(callback_query: types.CallbackQuery):
    await select_color(callback_query)


@dp.callback_query(Text(startswith='add_cart_'))
async def handle_add_to_cart(callback_query: types.CallbackQuery):
    await add_to_cart(callback_query)


@dp.callback_query(Text(startswith='buy_now_'))
async def handle_buy_now_cb(callback_query: types.CallbackQuery):
    await buy_now(callback_query, user_states[callback_query.from_user.id])


@dp.callback_query(Text(startswith='back_to_category_'))
async def handle_back_to_category_cb(callback_query: types.CallbackQuery):
    await back_to_category(callback_query)


@dp.message(lambda m: 'purchase' in user_states.get(m.from_user.id, {}))
async def handle_delivery_address_msg(message: types.Message):
    await handle_delivery_address(message, user_states[message.from_user.id])


@dp.callback_query(Text(startswith='confirm_order_'))
async def handle_confirm_order_cb(callback_query: types.CallbackQuery):
    await confirm_order(callback_query, user_states[callback_query.from_user.id])


@dp.callback_query(Text(startswith='payment_done_'))
async def handle_payment_done(callback_query: types.CallbackQuery):
    await payment_done(callback_query)


@dp.callback_query(Text('my_orders'))
async def handle_my_orders(callback_query: types.CallbackQuery):
    await my_orders(callback_query)


@dp.callback_query(Text('game'))
async def handle_game(callback_query: types.CallbackQuery):
    await game(callback_query)


@dp.callback_query(Text('admin_orders'))
async def handle_admin_orders(callback_query: types.CallbackQuery):
    await admin_orders(callback_query)


@dp.callback_query(Text('admin_stats'))
async def handle_admin_stats(callback_query: types.CallbackQuery):
    await admin_stats(callback_query)


@dp.callback_query(Text(startswith='confirm_payment_'))
async def handle_confirm_payment_cb(callback_query: types.CallbackQuery):
    await confirm_payment(callback_query)


@dp.callback_query(Text(startswith='mark_shipped_'))
async def handle_mark_shipped_cb(callback_query: types.CallbackQuery):
    await mark_shipped(callback_query)


@dp.callback_query(Text(startswith='mark_delivered_'))
async def handle_mark_delivered_cb(callback_query: types.CallbackQuery):
    await mark_delivered(callback_query)


@dp.callback_query(Text(startswith='cancel_order_'))
async def handle_cancel_order_cb(callback_query: types.CallbackQuery):
    await cancel_order(callback_query)


@dp.callback_query(Text(startswith='send_link_'))
async def handle_send_link_cb(callback_query: types.CallbackQuery):
    await send_link(callback_query, bot)


async def main():
    logger.info('Starting bot...')
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    asyncio.run(main())

