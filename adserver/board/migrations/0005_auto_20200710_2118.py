# Generated by Django 3.0.5 on 2020-07-10 18:18

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0004_auto_20200628_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='necessary_fields',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.jsonb.JSONField(), blank=True, null=True, size=None),
        ),
    ]
