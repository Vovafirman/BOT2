import logging
from aiogram import types

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

async def start(message: types.Message):
    """Handle /start command"""
    user = message.from_user
    db.add_user(user.id, user.username, user.first_name, user.last_name)
    await message.answer(
        get_welcome_message(),
        parse_mode="Markdown",
        reply_markup=get_start_keyboard(),
    )

async def open_store(callback_query: types.CallbackQuery):
    """Open the main menu from start button"""
    await callback_query.answer()
    await callback_query.message.edit_text(
        get_main_menu_message(),
        parse_mode="Markdown",
        reply_markup=get_main_menu_keyboard(),
    )

async def main_menu(callback_query: types.CallbackQuery):
    """Return to main menu"""
    await callback_query.answer()
    await callback_query.message.edit_text(
        get_main_menu_message(),
        parse_mode="Markdown",
        reply_markup=get_main_menu_keyboard(),
    )
