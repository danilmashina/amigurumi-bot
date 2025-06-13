import os
import requests
import telebot

# Получаем токены из переменных окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    raise Exception("Не заданы переменные окружения TELEGRAM_TOKEN и/или OPENAI_API_KEY!")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

@bot.message_handler(func=lambda message: True)
def generate_amigurumi(message):
    user_input = message.text.strip()

    if not user_input:
        bot.send_message(message.chat.id, "Пожалуйста, пришлите описание амигуруми для генерации схемы.")
        return

    prompt = (
        "Сгенерируй простую и понятную схему вязания амигуруми по следующему описанию: "
        f"{user_input}. "
        "Начни с кольца амигуруми, опиши материалы, голову, туловище, уши и другие части."
    )

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 800
    }

    try:
        response = requests.post(OPENAI_API_URL, json=payload, headers=headers, timeout=30)
        response.raise_for_status()  # выбросит ошибку при статусе != 2xx

        result = response.json()

        answer = result["choices"][0]["message"]["content"]
        bot.send_message(message.chat.id, answer)

    except requests.exceptions.RequestException as e:
        bot.send_message(message.chat.id, f"Произошла ошибка при подключении к OpenAI API:\n{e}")
        print("Ошибка подключения:", e)

    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла непредвиденная ошибка:\n{e}")
        print("Ошибка:", e)


if __name__ == "__main__":
    print("Бот запущен!")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
