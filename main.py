import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from telegram.error import TelegramError

from config import BOT_TOKEN, SUPPORT_USERNAME
from handlers.start import start, open_store, main_menu
from handlers.catalog import (
    catalog, show_category, show_product, select_color, 
    add_to_cart, buy_now, back_to_category, handle_delivery_address,
    confirm_order, payment_done
)
from handlers.orders import my_orders
from handlers.game import game
from handlers.admin import (
    admin_panel, admin_orders, admin_stats, manage_order,
    confirm_payment, mark_shipped, mark_delivered, cancel_order,
    send_link,
)
from utils.keyboards import get_back_to_main_keyboard

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def help_handler(update: Update, context):
    """Handle help button - redirect to support"""
    try:
        query = update.callback_query
        await query.answer()
        
        message = f"""
❓ **ПОМОЩЬ**

Для получения помощи обратитесь к нашему оператору:

👤 {SUPPORT_USERNAME}

Оператор поможет вам с:
• Вопросами по заказам
• Проблемами с оплатой  
• Выбором размеров
• Любыми другими вопросами

Время работы: 9:00 - 21:00 (МСК)
"""
        
        await query.edit_message_text(
            text=message,
            parse_mode='Markdown',
            reply_markup=get_back_to_main_keyboard()
        )
        
    except Exception as e:
        logger.error(f"Error in help handler: {e}")

async def error_handler(update: Update, context):
    """Handle errors"""
    logger.error(f"Update {update} caused error {context.error}")
    
    if update and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "Произошла ошибка. Попробуйте позже или обратитесь в поддержку."
            )
        except TelegramError:
            pass

def main():
    """Main function to run the bot"""
    try:
        # Create application
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Command handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("admin", admin_panel))
        
        # Dynamic command handler for order management
        application.add_handler(MessageHandler(
            filters.Regex(r'^/manage_\d+$') & filters.ChatType.PRIVATE,
            manage_order
        ))
        
        # Callback handlers
        application.add_handler(CallbackQueryHandler(open_store, pattern="^open_store$"))
        application.add_handler(CallbackQueryHandler(main_menu, pattern="^main_menu$"))
        
        # Catalog handlers
        application.add_handler(CallbackQueryHandler(catalog, pattern="^catalog$"))
        application.add_handler(CallbackQueryHandler(show_category, pattern="^category_"))
        application.add_handler(CallbackQueryHandler(show_product, pattern="^product_"))
        application.add_handler(CallbackQueryHandler(select_color, pattern="^color_"))
        application.add_handler(CallbackQueryHandler(add_to_cart, pattern="^add_cart_"))
        application.add_handler(CallbackQueryHandler(buy_now, pattern="^buy_now_"))
        application.add_handler(CallbackQueryHandler(back_to_category, pattern="^back_to_category_"))
        
        # New order flow handlers
        application.add_handler(CallbackQueryHandler(confirm_order, pattern="^confirm_order_"))
        application.add_handler(CallbackQueryHandler(payment_done, pattern="^payment_done_"))
        
        # Other menu handlers
        application.add_handler(CallbackQueryHandler(my_orders, pattern="^my_orders$"))
        application.add_handler(CallbackQueryHandler(game, pattern="^game$"))
        application.add_handler(CallbackQueryHandler(help_handler, pattern="^help$"))
        
        # Admin handlers
        application.add_handler(CallbackQueryHandler(admin_orders, pattern="^admin_orders$"))
        application.add_handler(CallbackQueryHandler(admin_stats, pattern="^admin_stats$"))
        application.add_handler(CallbackQueryHandler(confirm_payment, pattern="^confirm_payment_"))
        application.add_handler(CallbackQueryHandler(mark_shipped, pattern="^mark_shipped_"))
        application.add_handler(CallbackQueryHandler(mark_delivered, pattern="^mark_delivered_"))
        application.add_handler(CallbackQueryHandler(cancel_order, pattern="^cancel_order_"))
        application.add_handler(CallbackQueryHandler(send_link, pattern="^send_link_"))
        
        # Text message handler for delivery address (must be last)
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_delivery_address))
        
        # Error handler
        application.add_error_handler(error_handler)
        
        # Start the bot
        logger.info("Starting bot...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        logger.error(f"Error starting bot: {e}")

if __name__ == '__main__':
    main()