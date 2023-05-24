from django.contrib import admin
from telegram.models import TelegramId, BotToken


admin.site.register(TelegramId)
admin.site.register(BotToken)
