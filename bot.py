import os
import requests
import telebot
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("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")

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
            "Content-Type": "application/json",
            "HTTP-Referer": "https://t.me/YourAmigurumiBot",  # 🔥 УКАЖИ здесь свой Telegram бот/сайт
            "X-Title": "YourAmigurumi",  # 🔥 Название твоего бота или сайта
        }

        payload = {
            "model": "qwen/qwen3-235b-a22b:free",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 800
        }

        response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        answer = result["choices"][0]["message"]["content"]

        bot.send_message(message.chat.id, answer)

    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")

if __name__ == "__main__":
    print("🤖 Бот запущен...")
    bot.polling()
