from django.db import models
from django.db.models import Avg
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
            return f'({self.payment}) {self.fiat.abbr} - {self.asset.abbr} - {self.price_average}'
        else:
            return f'({self.payment}) {self.asset.abbr} - {self.fiat.abbr} - {self.price_average}'

    @property
    def price_average(self):
        return self.deal_set.aggregate(Avg('price'))['price__avg']

    @property
    def tooltip(self):
        return self.deal_set.order_by('price').first()


class Deal(models.Model):
    seller = models.CharField(max_length=45)
    price = models.FloatField()
    amount = models.FloatField()
    min_amount = models.FloatField(default=0)
    max_amount = models.FloatField(default=0)
    pair = models.ForeignKey(Pair, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return f'({self.pair}) - {self.amount}'


class Chain2(models.Model):
    buy_pair = models.ForeignKey(Pair, related_name='buy_pair', on_delete=models.CASCADE, default=0)
    sell_pair = models.ForeignKey(Pair, related_name='sell_pair', on_delete=models.CASCADE, default=0)
    profit = models.FloatField(default=0)

    def __str__(self):
        return f'{self.buy_pair.payment} -> {self.buy_pair.asset} -> {self.sell_pair.payment}'

    @property
    def profit_percentage(self):
        return round((self.profit - 1) * 100, 2)

    @profit_percentage.setter
    def profit_percentage(self, value):
        self.profit = value


class Chain2Reverse(models.Model):
    forward_chain = models.ForeignKey(Chain2, related_name='forward_chain', on_delete=models.CASCADE, default=0)
    backward_chain = models.ForeignKey(Chain2, related_name='backward_chain', on_delete=models.CASCADE, default=0)
    profit = models.FloatField(default=0)

    @property
    def profit_percentage(self):
        return round((self.profit - 1) * 100, 2)

    @profit_percentage.setter
    def profit_percentage(self, value):
        self.profit = value


class CurrenciesSpot(models.Model):
    asset1 = models.ForeignKey(Currency, related_name='asset1', on_delete=models.CASCADE, default=0)
    asset2 = models.ForeignKey(Currency, related_name='asset2', on_delete=models.CASCADE, default=0)
    rate = models.FloatField(default=0)

    def __str__(self):
        return f'1 {self.asset1.abbr} - {self.rate} {self.asset2.abbr}'

    @property
    def reverse_rate(self):
        return round(1/self.rate, 6)

    @reverse_rate.setter
    def reverse_rate(self, value):
        self.rate = value


class Chain3(models.Model):
    buy_pair = models.ForeignKey(Pair, related_name='buy_pair_chain3', on_delete=models.CASCADE, default=0)
    spot = models.ForeignKey(CurrenciesSpot, related_name='spot', on_delete=models.CASCADE, default=0)
    sell_pair = models.ForeignKey(Pair, related_name='sell_pair_chain3', on_delete=models.CASCADE, default=0)
    profit = models.FloatField(default=0)

    def __str__(self):
        return f'{self.buy_pair.payment} -> {self.buy_pair.asset} -> {self.sell_pair.asset} -> {self.sell_pair.payment}'

    @property
    def profit_percentage(self):
        return round((self.profit - 1) * 100, 2)

    @profit_percentage.setter
    def profit_percentage(self, value):
        self.profit = value


class Chain3Reverse(models.Model):
    forward_chain = models.ForeignKey(Chain3, related_name='forward_chain3', on_delete=models.CASCADE, default=0)
    backward_chain = models.ForeignKey(Chain3, related_name='backward_chain3', on_delete=models.CASCADE, default=0)
    profit = models.FloatField(default=0)

    @property
    def profit_percentage(self):
        return round((self.profit - 1) * 100, 2)

    @profit_percentage.setter
    def profit_percentage(self, value):
        self.profit = value