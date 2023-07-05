from django.contrib import admin
from currency.models import Currency, Pair, Payment, Deal, Chain2, Chain2Reverse, CurrenciesSpot, Chain3, Chain3Reverse

admin.site.register(Currency)
admin.site.register(Payment)
admin.site.register(Deal)
admin.site.register(Pair)
admin.site.register(Chain2)
admin.site.register(Chain2Reverse)
admin.site.register(CurrenciesSpot)
admin.site.register(Chain3)
admin.site.register(Chain3Reverse)
