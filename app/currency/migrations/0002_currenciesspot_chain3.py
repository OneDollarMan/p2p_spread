# Generated by Django 4.2.2 on 2023-07-04 17:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrenciesSpot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.FloatField(default=0)),
                ('asset1', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='asset1', to='currency.currency')),
                ('asset2', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='asset2', to='currency.currency')),
            ],
        ),
        migrations.CreateModel(
            name='Chain3',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profit', models.FloatField(default=0)),
                ('buy_pair', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='buy_pair_chain3', to='currency.pair')),
                ('sell_pair', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='sell_pair_chain3', to='currency.pair')),
                ('spot', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='spot', to='currency.currenciesspot')),
            ],
        ),
    ]