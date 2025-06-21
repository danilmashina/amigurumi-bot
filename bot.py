import os
import requests
import telebot
from dotenv import load_dotenv

# Загрузка переменных окружения из .env (если запускаешь локально)
load_dotenv()

# Получение токенов из окружения
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("Bearer OPENROUTER_API_KEY")

# Проверка на наличие переменных
if not TELEGRAM_TOKEN or not OPENROUTER_API_KEY:
    raise ValueError("BOT_TOKEN или OPENROUTER_API_KEY не заданы!")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

@bot.message_handler(func=lambda message: True)
def generate_amigurumi(message):
    user_input = message.text

    prompt = f"""
    Сгенерируй простую и понятную схему вязания амигуруми по следующему описанию: {user_input}.
    Начни с кольца амигуруми, опиши материалы, голову, туловище, уши и другие части.
    """

    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "qwen/qwen3-235b-a22b:free",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 800
        }

        response = requests.post(OPENROUTER_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        answer = result["choices"][0]["message"]["content"]

        bot.send_message(message.chat.id, answer)

    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {str(e)}")

# Запуск бота
if __name__ == "__main__":
    print("🤖 Бот запущен...")
    bot.polling()
