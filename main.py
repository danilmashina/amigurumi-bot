import os
import requests
import telebot

# Получаем токены из переменных окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not TELEGRAM_TOKEN or not OPENROUTER_API_KEY:
    raise Exception("Не заданы переменные окружения TELEGRAM_TOKEN и/или OPENROUTER_API_KEY!")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Адрес OpenRouter API
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Обработчик всех входящих сообщений
@bot.message_handler(func=lambda message: True)
def generate_amigurumi(message):
    user_input = message.text

    # Формируем промпт для модели
    prompt = (
        "Сгенерируй простую и понятную схему вязания амигуруми по следующему описанию: "
        f"{user_input}. "
        "Начни с кольца амигуруми, опиши материалы, голову, туловище, уши и другие части."
    )

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",  # или другая модель, доступная в OpenRouter
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 800
    }

    try:
        response = requests.post(OPENROUTER_API_URL, json=payload, headers=headers)
        print("STATUS CODE:", response.status_code)
        print("RESPONSE TEXT:", response.text)

        if response.status_code != 200:
            raise Exception(f"OpenRouter API вернул ошибку {response.status_code}: {response.text}")

        result = response.json()
        answer = result["choices"][0]["message"]["content"]

        bot.send_message(message.chat.id, answer)

    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка:\n{e}")
        print("ОШИБКА:", e)

if __name__ == "__main__":
    print("Бот запущен!")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
