from django.contrib import admin
from currency.models import Currency, Pair, Payment, Deal

admin.site.register(Currency)
admin.site.register(Payment)
admin.site.register(Deal)
admin.site.register(Pair)
