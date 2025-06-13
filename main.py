import requests
import telebot

# Токен Telegram-бота
bot = telebot.TeleBot('7769564086:AAGjVg1dyk-bnR2Uc8U58u1-5cWTKuFKduM')

# OpenRouter API
OPENROUTER_API_URL = "https://openrouter.ai/v1/chat/completions"
OPENROUTER_API_KEY = "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"

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
            "HTTP-Referer": "https://example.com",  # обязателен!
            "X-Title": "amigurumi-bot"
        }

        payload = {
            "model": "anthropic/claude-3-haiku",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 800
        }

        response = requests.post(OPENROUTER_API_URL, json=payload, headers=headers)

        # Выводим отладочную информацию
        print("STATUS CODE:", response.status_code)
        print("RESPONSE TEXT:", response.text)

        # Проверяем, есть ли тело
        if response.status_code != 200:
            raise Exception(f"OpenRouter вернул ошибку {response.status_code}: {response.text}")

        result = response.json()
        answer = result["choices"][0]["message"]["content"]

        bot.send_message(message.chat.id, answer)

    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка:\n{e}")
        print("ОШИБКА:", e)

# Запуск бота
bot.polling()
