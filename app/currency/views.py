from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django_celery_beat.models import PeriodicTask

from currency.models import Deal, Currency, Chain2, Chain2Reverse


def index(request):
    context = {
        'title': 'Главная'
    }
    return render(request, 'currency/index.html', context)


@login_required
def changes(request):
    context = {
        'title': 'Цепочки сделок',
        'time': PeriodicTask.objects.get(task='currency.tasks.get_deals').last_run_at,
        'chain2': Chain2.objects.filter(buy_pair__fiat__abbr='RUB').order_by('-profit')[:10],
        'chain2reverse': Chain2Reverse.objects.filter(forward_chain__buy_pair__fiat__abbr='RUB').order_by('-profit')[:10]
    }
    return render(request, 'currency/changes.html', context)


@login_required
def rates(request):
    context = {
        'title': 'Сделки',
        'assets': Currency.objects.filter(is_fiat=0),
        'deals_RaiffeisenBank_rub_buy': Deal.objects.filter(pair__fiat__abbr='RUB', pair__payment__binance_name='RaiffeisenBank', pair__trade_type='BUY'),
        'deals_RaiffeisenBank_rub_sell': Deal.objects.filter(pair__fiat__abbr='RUB', pair__payment__binance_name='RaiffeisenBank', pair__trade_type='SELL'),
        'deals_TinkoffNew_rub_buy': Deal.objects.filter(pair__fiat__abbr='RUB', pair__payment__binance_name='TinkoffNew', pair__trade_type='BUY'),
        'deals_TinkoffNew_rub_sell': Deal.objects.filter(pair__fiat__abbr='RUB', pair__payment__binance_name='TinkoffNew', pair__trade_type='SELL'),
        'deals_YandexMoneyNew_rub_buy': Deal.objects.filter(pair__fiat__abbr='RUB', pair__payment__binance_name='YandexMoneyNew', pair__trade_type='BUY'),
        'deals_YandexMoneyNew_rub_sell': Deal.objects.filter(pair__fiat__abbr='RUB', pair__payment__binance_name='YandexMoneyNew', pair__trade_type='SELL'),
        'deals_QIWI_rub_buy': Deal.objects.filter(pair__fiat__abbr='RUB', pair__payment__binance_name='QIWI', pair__trade_type='BUY'),
        'deals_QIWI_rub_sell': Deal.objects.filter(pair__fiat__abbr='RUB', pair__payment__binance_name='QIWI', pair__trade_type='SELL'),
        'time': PeriodicTask.objects.get(task='currency.tasks.get_deals').last_run_at
    }
    return render(request, 'currency/rates.html', context)


@login_required
def donate(request):
    context = {
        'title': 'Донат'
    }
    return render(request, 'currency/donate.html', context)