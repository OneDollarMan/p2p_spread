from django.db import models
from django.utils.translation import gettext_lazy as _


class Currency(models.Model):
    name = models.CharField(max_length=45)
    abbr = models.CharField(max_length=4)
    is_fiat = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name} ({self.abbr})'


class Payment(models.Model):
    name = models.CharField(max_length=45)
    binance_name = models.CharField(max_length=45, default='test')

    def __str__(self):
        return self.name


class Pair(models.Model):
    asset = models.ForeignKey(Currency, related_name='asset', on_delete=models.CASCADE, default=0)
    fiat = models.ForeignKey(Currency, related_name='fiat', on_delete=models.CASCADE, default=0)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, default=0)

    class TradeType(models.TextChoices):
        BUY = 'BUY', _('Покупка')
        SELL = 'SELL', _('Продажа')

    trade_type = models.CharField(max_length=4, choices=TradeType.choices, default=TradeType.BUY)

    def __str__(self):
        if self.trade_type == self.TradeType.BUY:
            return f'({self.payment}) {self.fiat.abbr} - {self.asset.abbr}'
        else:
            return f'({self.payment}) {self.asset.abbr} - {self.fiat.abbr}'


class Deal(models.Model):
    seller = models.CharField(max_length=45)
    price = models.FloatField()
    amount = models.FloatField()
    pair = models.ForeignKey(Pair, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return f'({self.pair}) {self.price} - {self.amount}'
