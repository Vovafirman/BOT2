from .start import start, open_store, main_menu
from .catalog import (
    catalog,
    show_category,
    show_product,
    select_color,
    add_to_cart,
    buy_now,
    back_to_category,
    handle_delivery_address,
    confirm_order,
    payment_done,
)
from .orders import my_orders
from .game import game
from .admin import (
    admin_panel,
    admin_orders,
    admin_stats,
    manage_order,
    confirm_payment,
    mark_shipped,
    mark_delivered,
    cancel_order,
    send_link,
)

__all__ = [
    'start', 'open_store', 'main_menu',
    'catalog', 'show_category', 'show_product', 'select_color', 'add_to_cart', 'buy_now', 'back_to_category', 'handle_delivery_address', 'confirm_order', 'payment_done',
    'my_orders',
    'game',
    'admin_panel', 'admin_orders', 'admin_stats', 'manage_order', 'confirm_payment', 'mark_shipped', 'mark_delivered', 'cancel_order', 'send_link',
]

