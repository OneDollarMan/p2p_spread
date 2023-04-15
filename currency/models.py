from django.db import models


class Currency(models.Model):
    name = models.CharField(max_length=32)
    abbr = models.CharField(max_length=4)
    current_usd_price = models.DecimalField(decimal_places=10, max_digits=19)

    def __str__(self):
        return self.name


class Pair(models.Model):
    currency1 = models.ForeignKey(Currency, related_name='currency1', on_delete=models.CASCADE, default=0)
    currency2 = models.ForeignKey(Currency, related_name='currency2', on_delete=models.CASCADE, default=0)
