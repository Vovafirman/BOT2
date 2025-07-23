import logging
from telegram import Update
from telegram.ext import ContextTypes

from config import ADMIN_IDS
from database import db
from utils.keyboards import (
    get_start_keyboard,
    get_main_menu_keyboard,
)
from utils.messages import (
    get_welcome_message,
    get_main_menu_message,
)

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    db.add_user(user.id, user.username, user.first_name, user.last_name)
    await update.message.reply_text(
        get_welcome_message(),
        parse_mode="Markdown",
        reply_markup=get_start_keyboard(),
    )

async def open_store(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Open the main menu from start button"""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        get_main_menu_message(),
        parse_mode="Markdown",
        reply_markup=get_main_menu_keyboard(),
    )

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Return to main menu"""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        get_main_menu_message(),
        parse_mode="Markdown",
        reply_markup=get_main_menu_keyboard(),
    )
