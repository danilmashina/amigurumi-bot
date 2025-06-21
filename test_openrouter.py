import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY не задан!")

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    # Можно убрать эти заголовки, если хочешь
    # "HTTP-Referer": "https://t.me/YourAmigurumiBot",
    # "X-Title": "YourAmigurumi",
}

payload = {
    "model": "qwen/qwen3-235b-a22b:free",
    "messages": [
        {"role": "user", "content": "What is the meaning of life?"}
    ],
    "temperature": 0.7,
    "max_tokens": 100
}

response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload)

print("Статус:", response.status_code)
print("Заголовки ответа:", response.headers)
print("Тело ответа:", response.text)

try:
    response.raise_for_status()
    data = response.json()
    print("Ответ API:", data)
except requests.exceptions.HTTPError as e:
    print("Ошибка HTTP:", e)
