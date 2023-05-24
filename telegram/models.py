from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save


class TelegramId(models.Model):
    telegram_id=models.BigIntegerField(unique=True)

    def __str__(self):
        return str(self.telegram_id)


class BotToken(models.Model):
    bot_token = models.CharField(max_length=64)

    def __str__(self):
        return self.bot_token


@receiver(pre_save, sender=BotToken)
def pre_save_bot_token(*args, **kwargs):
    BotToken.objects.all().delete()
