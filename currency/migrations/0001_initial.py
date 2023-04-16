# Generated by Django 4.1.7 on 2023-04-15 09:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('abbr', models.CharField(max_length=4)),
                ('is_fiat', models.BinaryField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Pair',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency1', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='currency1', to='currency.currency')),
                ('currency2', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='currency2', to='currency.currency')),
                ('payment', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='currency.payment')),
            ],
        ),
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seller', models.IntegerField()),
                ('price', models.FloatField()),
                ('amount', models.FloatField()),
                ('pair', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='currency.pair')),
            ],
        ),
    ]
