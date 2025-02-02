import os
import requests
import re
from background import keep_alive
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackContext

# Получение переменных окружения
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
HUGGING_FACE_API_KEY = os.environ.get('HUGGING_FACE_API_KEY')
MODEL_URL = os.environ.get('https://api-inference.huggingface.co/models/mistralai/Mistral-Nemo-Instruct-2407') 


async def generate_joke():
    headers = {'Authorization': f'Bearer {HUGGING_FACE_API_KEY}'}
    payload = {
        'inputs': "Сгенерируй новую абсурдную шутку про пельмени:",
        'parameters': {
            'max_length': 50,
            'num_return_sequences': 1,
            'do_sample': True,
            'temperature': 0.7,
            'top_k': 50,
            'top_p': 0.95,
            'repetition_penalty': 1.2,
            'return_full_text': False
        },
        'options': {'use_cache': False}
    }

    try:
        response = requests.post(MODEL_URL, headers=headers, json=payload)
        response.raise_for_status()

        if response.status_code == 200:
            output = response.json()
            if isinstance(output, list) and len(output) > 0:
                return output[0].get('generated_text', 'Шутка сбежала в кулинарную книгу!').strip()

        return "Сегодня пельмени отдыхают. Попробуй позже!"

    except Exception as e:
        return f"Ошибка на кухне: {e}"

async def handle_message(update: Update, context: CallbackContext):
    if re.search(r'\bпельмени\b', update.message.text.lower()):
        joke = await generate_joke()
        await update.message.reply_text(joke)

def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Бот-шутец запущен!")
    application.run_polling()

keep_alive()

if __name__ == "__main__":
    main()
