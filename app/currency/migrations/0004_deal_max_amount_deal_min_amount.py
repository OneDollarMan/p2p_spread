# Generated by Django 4.2.2 on 2023-07-06 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0003_chain3reverse'),
    ]

    operations = [
        migrations.AddField(
            model_name='deal',
            name='max_amount',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='deal',
            name='min_amount',
            field=models.FloatField(default=0),
        ),
    ]
