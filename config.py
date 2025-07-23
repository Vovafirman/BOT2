import os
import logging

# Bot configuration
BOT_TOKEN = os.getenv("BOT_TOKEN", "8076821995:AAGUehKkk_EagiZWJgPd3MQs7iT5LzR-wFU")
DATABASE_URL = "cinema_merch.db"
GAME_URL = "https://center-kino.github.io/game_kinoshlep/"
SUPPORT_USERNAME = "@PRdemon"

# Admin user IDs (add your admin user IDs here)
ADMIN_IDS = [123456789]  # Replace with actual admin user IDs

# Product categories
CATEGORIES = {
    "center_kino": "Футболки \"Центр Кино\"",
    "kinomechanika": "Футболки \"Киномеханки\"",
    "board_games": "Настольные игры"
}

# Product data
PRODUCTS = {
    # Центр Кино футболки
    "original": {
        "name": "Оригинал",
        "category": "center_kino",
        "price": 2250,
        "size": "OVERSIZE",
        "density": "240 грамм",
        "material": "Хлопок",
        "colors": ["МОЛОЧНЫЙ", "ЧЕРНЫЙ"],
        "image": "photo_1.jpg"
    },
    "director": {
        "name": "Режиссер",
        "category": "center_kino",
        "price": 2250,
        "size": "OVERSIZE",
        "density": "240 грамм",
        "material": "Хлопок",
        "colors": ["МОЛОЧНЫЙ", "ЧЕРНЫЙ"],
        "image": "photo_2.jpg"
    },
    "scenario": {
        "name": "Сценарий",
        "category": "center_kino",
        "price": 2250,
        "size": "OVERSIZE",
        "density": "240 грамм",
        "material": "Хлопок",
        "colors": ["МОЛОЧНЫЙ", "ЧЕРНЫЙ"],
        "image": "photo_3.jpg"
    },
    "watch_till_end": {
        "name": "Смотри до конца",
        "category": "center_kino",
        "price": 2250,
        "size": "OVERSIZE",
        "density": "240 грамм",
        "material": "Хлопок",
        "colors": ["МОЛОЧНЫЙ", "ЧЕРНЫЙ"],
        "image": "photo_4.jpg"
    },
    "episode_meaning": {
        "name": "Даже в эпизоде есть смысл",
        "category": "center_kino",
        "price": 2250,
        "size": "OVERSIZE",
        "density": "240 грамм",
        "material": "Хлопок",
        "colors": ["МОЛОЧНЫЙ", "ЧЕРНЫЙ"],
        "image": "photo_5.jpg"
    },
    "after_credits": {
        "name": "После титров",
        "category": "center_kino",
        "price": 2250,
        "size": "OVERSIZE",
        "density": "240 грамм",
        "material": "Хлопок",
        "colors": ["МОЛОЧНЫЙ", "ЧЕРНЫЙ"],
        "image": "photo_6.jpg"
    },
    "comedy": {
        "name": "Комедия",
        "category": "center_kino",
        "price": 2250,
        "size": "OVERSIZE",
        "density": "240 грамм",
        "material": "Хлопок",
        "colors": ["МОЛОЧНЫЙ", "ЧЕРНЫЙ"],
        "image": "photo_7.jpg"
    },
    # Киномеханки футболки
    "projector_watcher": {
        "name": "Смотрящий за проектором",
        "category": "kinomechanika",
        "price": 2250,
        "size": "OVERSIZE",
        "density": "240 грамм",
        "material": "Хлопок",
        "colors": ["ЧЕРНЫЙ"],
        "image": "photo_8.jpg"
    },
    "not_scary_film": {
        "name": "Не так страшен фильм",
        "category": "kinomechanika",
        "price": 2250,
        "size": "OVERSIZE",
        "density": "240 грамм",
        "material": "Хлопок",
        "colors": ["ЧЕРНЫЙ"],
        "image": "photo_9.jpg"
    },
    "will_there_be_cinema": {
        "name": "А кино будет?",
        "category": "kinomechanika",
        "price": 2250,
        "size": "OVERSIZE",
        "density": "240 грамм",
        "material": "Хлопок",
        "colors": ["ЧЕРНЫЙ"],
        "image": "photo_10.jpg"
    },
    "where_is_key": {
        "name": "А где ключ?",
        "category": "kinomechanika",
        "price": 2250,
        "size": "OVERSIZE",
        "density": "240 грамм",
        "material": "Хлопок",
        "colors": ["ЧЕРНЫЙ"],
        "image": "photo_11.jpg"
    },
    "kinomechanic": {
        "name": "Киномеханик",
        "category": "kinomechanika",
        "price": 2250,
        "size": "OVERSIZE",
        "density": "240 грамм",
        "material": "Хлопок",
        "colors": ["ЧЕРНЫЙ"],
        "image": "photo_12.jpg"
    },
    "signed_edo": {
        "name": "Подписал ЭДО?",
        "category": "kinomechanika",
        "price": 2250,
        "size": "OVERSIZE",
        "density": "240 грамм",
        "material": "Хлопок",
        "colors": ["ЧЕРНЫЙ"],
        "image": "photo_13.jpg"
    },
    # Настольные игры
    "board_game_film": {
        "name": "Снимим, если сможешь",
        "category": "board_games",
        "price": 3500,
        "description": "Возрастные ограничения: 12+ лет\nКлассификация: Развлекательная / Стратегия\nКоличество игроков: от 3-ех до 6 человек\n\nВозможно вы будущий продюсер?!\nА может ваши друзья?!\nКто сможет первый снять 3 фильма?!",
        "image": "photo_14.jpg"
    }
}

# Logging configuration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
