# Generated by Django 3.0.5 on 2020-07-07 23:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0004_auto_20200628_1659'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0002_message_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dialogue',
            name='ad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dialogues', to='board.Ad'),
        ),
        migrations.AlterField(
            model_name='message',
            name='recipient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='recipient_messages', to=settings.AUTH_USER_MODEL),
        ),
    ]
