def get_welcome_message():
    """Get welcome message"""
    return """
🎬 Добро пожаловать! 🎬

Уважаемые пользователи, рады приветствовать Вас в нашем магазине мерча от компании **Центр Кино**!

Здесь вы найдете:
• Эксклюзивные футболки с киношной тематикой
• Настольные игры для киноманов
• Увлекательную игру "Киношлёп"

Для начала покупок нажмите кнопку ниже ⬇️
"""

def get_main_menu_message():
    """Get main menu message"""
    return """
🎬 **ЦЕНТР КИНО МЕРЧ** 🎬

Главное меню:

📚 **Каталог товаров** - просмотр всех наших товаров
📦 **Мои заказы** - отслеживание ваших покупок  
🎮 **Игра "Киношлёп"** - увлекательная игра для киноманов
❓ **Помощь** - связь с оператором

Выберите нужный раздел:
"""

def get_catalog_message():
    """Get catalog message"""
    return """
📚 **КАТАЛОГ ТОВАРОВ**

Выберите категорию:

👕 **Футболки "Центр Кино"** - оригинальные дизайны
👕 **Футболки "Киномеханки"** - для профессионалов
🎲 **Настольные игры** - для компании друзей

Все футболки:
• Размер: OVERSIZE
• Плотность: 240 грамм
• Материал: 100% хлопок
• Высокое качество печати
"""

def get_product_message(product):
    """Get product description message"""
    message = f"""
🏷️ **{product['name']}**

"""
    
    if product['category'] in ['center_kino', 'kinomechanika']:
        message += f"""📏 Размер: {product['size']}
⚖️ Плотность: {product['density']}
🧵 Материал: {product['material']}
💰 Цена: {product['price']} рублей

"""
    else:
        message += f"""📝 {product.get('description', '')}
💰 Цена: {product['price']} рублей

"""
    
    if product['colors']:
        message += "🎨 Доступные цвета:\n"
        for color in product['colors']:
            message += f"• {color}\n"
        message += "\nВыберите цвет:"
    else:
        message += "Готовы к покупке?"
    
    return message

def get_game_message():
    """Get game message"""
    return """
🎮 **ИГРА "КИНОШЛЁП"**

Увлекательная игра для настоящих киноманов!

Проверьте свои знания кино, угадывайте фильмы по кадрам и соревнуйтесь с друзьями.

Нажмите кнопку ниже, чтобы начать играть:
"""

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
        order_id, product_key, color, quantity, total_price, status, payment_status, tracking_link, created_at, product_name = order
        
        status_emoji = {
            'pending': '⏳',
            'confirmed': '✅',
            'shipped': '📦',
            'delivered': '🎯',
            'cancelled': '❌'
        }.get(status, '❓')
        
        payment_emoji = {
            'unpaid': '💳',
            'paid': '✅',
            'refunded': '🔄'
        }.get(payment_status, '❓')
        
        message += f"""
{status_emoji} **Заказ #{order_id}**
📅 Дата: {created_at[:10]}
🏷️ Товар: {product_name}
"""
        
        if color and color != 'none':
            message += f"🎨 Цвет: {color}\n"
        
        message += f"""📊 Статус: {status}
{payment_emoji} Оплата: {payment_status}
💰 Сумма: {total_price} ₽
"""
        
        if tracking_link:
            message += f"🚚 Отслеживание: {tracking_link}\n"
        
        message += "─────────────────\n"
    
    return message

def get_help_message():
    """Get help message"""
    return """
❓ **ПОМОЩЬ**

Для получения помощи обратитесь к нашему оператору:

👤 @PRdemon

Оператор поможет вам с:
• Вопросами по заказам
• Проблемами с оплатой  
• Выбором размеров
• Любыми другими вопросами

Время работы: 9:00 - 21:00 (МСК)
"""

def get_cart_added_message(product_name, color=None):
    """Get message when product added to cart"""
    message = f"✅ Товар **{product_name}**"
    if color and color != 'none':
        message += f" (цвет: {color})"
    message += " добавлен в корзину!"
    return message

def get_delivery_request_message(product_name, color=None):
    """Get delivery address request message"""
    message = f"""
📋 **ОФОРМЛЕНИЕ ЗАКАЗА**

🏷️ Товар: {product_name}
"""
    
    if color and color != 'none':
        message += f"🎨 Цвет: {color}\n"
    
    message += """
📍 **Напишите адрес доставки:**

ФИО
Город проживания  
Адрес доставки
Индекс
Номер телефона

Отправьте все данные одним сообщением.
"""
    
    return message

def get_order_confirmation_message(product, color, delivery_address):
    """Get order confirmation message"""
    message = f"""
📋 **ПОДТВЕРЖДЕНИЕ ЗАКАЗА**

🏷️ Товар: {product['name']}
"""
    
    if product['category'] in ['center_kino', 'kinomechanika']:
        message += f"""📏 Размер: {product['size']}
⚖️ Плотность: {product['density']}
🧵 Материал: {product['material']}
"""
    
    message += f"💰 Цена: {product['price']} рублей\n"
    
    if color and color != 'none':
        message += f"🎨 Цвет: {color}\n"
    
    message += f"""
📍 **Адрес доставки:**
{delivery_address}

Всё верно?
"""
    
    return message

def get_payment_message(order_id):
    """Get payment message"""
    message = f"""
💳 **ОПЛАТА ЗАКАЗА #{order_id}**

Для оплаты перейдите по кнопке "Оплатить"

После того как оплатите, нажмите кнопку "Я оплатил"

Менеджер проверит оплату заказа и подтвердит ваш заказ
"""
    
    return message

def get_order_created_message(order_id, product_name, color=None, total_price=None):
    """Get message when order is created"""
    message = f"""
✅ **ЗАКАЗ ОФОРМЛЕН!**

📋 Номер заказа: #{order_id}
🏷️ Товар: {product_name}
"""
    
    if color and color != 'none':
        message += f"🎨 Цвет: {color}\n"
    
    if total_price:
        message += f"💰 Сумма: {total_price} ₽\n"
    
    message += """
📞 Наш менеджер свяжется с вами для подтверждения заказа и уточнения деталей доставки.

Спасибо за покупку! 🎬
"""
    
    return message

def get_admin_new_order_message(order_id, user, product_name, color, delivery_address, total_price):
    """Get admin notification message for new order"""
    user_info = f"@{user.username}" if user.username else f"{user.first_name or 'Unknown'}"
    
    message = f"""
🔔 **НОВЫЙ ЗАКАЗ #{order_id}**

👤 Пользователь: {user_info} (ID: {user.id})
🏷️ Товар: {product_name}
"""
    
    if color and color != 'none':
        message += f"🎨 Цвет: {color}\n"
    
    message += f"""💰 Сумма: {total_price} ₽

📍 **Адрес доставки:**
{delivery_address}

/manage_{order_id} - управление заказом
"""
    
    return message
