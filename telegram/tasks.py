from config.celery import app
import requests
from telegram.models import BotToken, TelegramId


@app.task()
def send_message_to_telegram(message):
    for BOT_TOKEN in BotToken.objects.all():
        for TELEGRAM_ID in TelegramId.objects.all():
            requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={TELEGRAM_ID}&text={message}")
