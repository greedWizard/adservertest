# Generated by Django 3.0.5 on 2020-07-08 08:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0004_auto_20200628_1659'),
        ('chat', '0003_auto_20200708_0236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dialogue',
            name='ad',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dialogues', to='board.Ad'),
        ),
    ]
