from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_start_keyboard():
    """Get start keyboard with 'Open Store' button"""
    keyboard = [
        [InlineKeyboardButton("🛍️ Открыть магазин", callback_data="open_store")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_main_menu_keyboard():
    """Get main menu keyboard"""
    keyboard = [
        [InlineKeyboardButton("📚 Каталог товаров", callback_data="catalog")],
        [InlineKeyboardButton("📦 Мои заказы", callback_data="my_orders")],
        [InlineKeyboardButton("🎮 Игра \"Киношлёп\"", callback_data="game")],
        [InlineKeyboardButton("❓ Помощь", callback_data="help")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_catalog_keyboard():
    """Get catalog categories keyboard"""
    keyboard = [
        [InlineKeyboardButton("👕 Футболки \"Центр Кино\"", callback_data="category_center_kino")],
        [InlineKeyboardButton("👕 Футболки \"Киномеханки\"", callback_data="category_kinomechanika")],
        [InlineKeyboardButton("🎲 Настольные игры", callback_data="category_board_games")],
        [InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_products_keyboard(products, category):
    """Get products keyboard for a category"""
    keyboard = []
    
    for product in products:
        product_key, name, price, image = product
        keyboard.append([InlineKeyboardButton(f"{name} - {price} ₽", callback_data=f"product_{product_key}")])
    
    keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="catalog")])
    return InlineKeyboardMarkup(keyboard)

def get_product_colors_keyboard(product_key, colors):
    """Get product colors keyboard"""
    keyboard = []
    
    for color in colors:
        keyboard.append([InlineKeyboardButton(f"Цвет: {color}", callback_data=f"color_{product_key}_{color}")])
    
    keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data=f"back_to_category_{product_key}")])
    return InlineKeyboardMarkup(keyboard)

def get_product_actions_keyboard(product_key, color=None):
    """Get product actions keyboard (for board games or after color selection)"""
    keyboard = []
    
    if color:
        keyboard.append([InlineKeyboardButton("🛒 Добавить в корзину", callback_data=f"add_cart_{product_key}_{color}")])
        keyboard.append([InlineKeyboardButton("💳 Купить сейчас", callback_data=f"buy_now_{product_key}_{color}")])
    else:
        keyboard.append([InlineKeyboardButton("🛒 Добавить в корзину", callback_data=f"add_cart_{product_key}_none")])
        keyboard.append([InlineKeyboardButton("💳 Купить сейчас", callback_data=f"buy_now_{product_key}_none")])
    
    keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data=f"back_to_category_{product_key}")])
    return InlineKeyboardMarkup(keyboard)

def get_delivery_request_keyboard(product_key, color):
    """Get keyboard for delivery address request"""
    keyboard = [
        [InlineKeyboardButton("🔙 Назад", callback_data=f"product_{product_key}")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_order_confirmation_keyboard(product_key, color):
    """Get order confirmation keyboard"""
    keyboard = [
        [InlineKeyboardButton("✅ Подтверждаю", callback_data=f"confirm_order_{product_key}_{color}")],
        [InlineKeyboardButton("❌ Отмена", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_payment_keyboard(order_id):
    """Get payment keyboard"""
    keyboard = [
        [InlineKeyboardButton("💳 Оплатить", url="https://your-payment-link.com")],  # Replace with actual payment link
        [InlineKeyboardButton("✅ Я оплатил", callback_data=f"payment_done_{order_id}")],
        [InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_game_keyboard():
    """Get game keyboard"""
    keyboard = [
        [InlineKeyboardButton("🎮 Играть в \"КИНОШЛЁП\"", url="https://center-kino.github.io/game_kinoshlep/")],
        [InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_orders_keyboard():
    """Get orders keyboard"""
    keyboard = [
        [InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_admin_keyboard():
    """Get admin keyboard"""
    keyboard = [
        [InlineKeyboardButton("📋 Все заказы", callback_data="admin_orders")],
        [InlineKeyboardButton("📊 Статистика", callback_data="admin_stats")],
        [InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_order_management_keyboard(order_id):
    """Get order management keyboard for admins"""
    keyboard = [
        [InlineKeyboardButton("✅ Подтвердить оплату", callback_data=f"confirm_payment_{order_id}")],
        [InlineKeyboardButton("📦 Отправлено", callback_data=f"mark_shipped_{order_id}")],
        [InlineKeyboardButton("🎯 Доставлено", callback_data=f"mark_delivered_{order_id}")],
        [InlineKeyboardButton("❌ Отменить", callback_data=f"cancel_order_{order_id}")],
        [InlineKeyboardButton("🔙 Назад", callback_data="admin_orders")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_to_main_keyboard():
    """Simple back to main menu keyboard"""
    keyboard = [
        [InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")]
    ]
    return InlineKeyboard