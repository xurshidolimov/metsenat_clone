# Generated by Django 4.1.7 on 2023-05-19 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramid',
            name='telegram_id',
            field=models.BigIntegerField(),
        ),
    ]