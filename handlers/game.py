from aiogram import types

from utils.keyboards import get_game_keyboard
from utils.messages import get_game_message

async def game(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text(
        get_game_message(),
        parse_mode='Markdown',
        reply_markup=get_game_keyboard(),
    )

