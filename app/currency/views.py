from django.shortcuts import render, redirect
from django_celery_beat.models import PeriodicTask

from currency import tasks
from currency.models import Deal, Currency, Chain2


def index(request):
    context = {
        'title': 'Главная',
        'assets': Currency.objects.filter(is_fiat=0),
        'deals_RaiffeisenBank_rub_buy': Deal.objects.filter(pair__fiat__abbr='RUB', pair__payment__binance_name='RaiffeisenBank', pair__trade_type='BUY'),
        'deals_RaiffeisenBank_rub_sell': Deal.objects.filter(pair__fiat__abbr='RUB', pair__payment__binance_name='RaiffeisenBank', pair__trade_type='SELL'),
        'deals_TinkoffNew_rub_buy': Deal.objects.filter(pair__fiat__abbr='RUB', pair__payment__binance_name='TinkoffNew', pair__trade_type='BUY'),
        'deals_TinkoffNew_rub_sell': Deal.objects.filter(pair__fiat__abbr='RUB', pair__payment__binance_name='TinkoffNew', pair__trade_type='SELL'),
        'deals_YandexMoneyNew_rub_buy': Deal.objects.filter(pair__fiat__abbr='RUB', pair__payment__binance_name='YandexMoneyNew', pair__trade_type='BUY'),
        'deals_YandexMoneyNew_rub_sell': Deal.objects.filter(pair__fiat__abbr='RUB', pair__payment__binance_name='YandexMoneyNew', pair__trade_type='SELL'),
        'deals_QIWI_rub_buy': Deal.objects.filter(pair__fiat__abbr='RUB', pair__payment__binance_name='QIWI', pair__trade_type='BUY'),
        'deals_QIWI_rub_sell': Deal.objects.filter(pair__fiat__abbr='RUB', pair__payment__binance_name='QIWI', pair__trade_type='SELL'),
        'time': PeriodicTask.objects.get(task='currency.tasks.get_deals').last_run_at,
        'chain2': Chain2.objects.order_by('-profit')[:10]
    }
    return render(request, 'currency/change.html', context)


def update(request):
    return redirect('index')
