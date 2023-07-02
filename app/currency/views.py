from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django_celery_beat.models import PeriodicTask

from currency import forms, service
from currency.models import Deal, Currency, Chain2, Chain2Reverse


def index(request):
    context = {
        'title': 'Главная'
    }
    return render(request, 'currency/index.html', context)


@login_required
def rates(request):
    context = {
        'title': 'Курсы валют',
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
def changes_chain2(request):
    if request.GET:
        form = forms.Chain2Form(request.GET)
        context = {
            'title': 'Спреды',
            'time': PeriodicTask.objects.get(task='currency.tasks.get_deals').last_run_at,
            'chain2': service.get_chain2_objects_filtered(form),
            'form': form,
        }
    else:
        context = {
            'title': 'Спреды',
            'time': PeriodicTask.objects.get(task='currency.tasks.get_deals').last_run_at,
            'chain2': service.get_chain2_objects_filtered(),
            'form': forms.Chain2Form(),
        }
    return render(request, 'currency/changes_chain2.html', context)


@login_required
def changes_chain2reverse(request):
    if request.GET:
        form = forms.Chain2ReverseForm(request.GET)
        context = {
            'title': 'Обратные спреды',
            'time': PeriodicTask.objects.get(task='currency.tasks.get_deals').last_run_at,
            'chain2reverse': service.get_chain2reverse_objects_filtered(form),
            'form': form
        }
    else:
        context = {
            'title': 'Обратные спреды',
            'time': PeriodicTask.objects.get(task='currency.tasks.get_deals').last_run_at,
            'chain2reverse': service.get_chain2reverse_objects_filtered(),
            'form': forms.Chain2ReverseForm()
        }
    return render(request, 'currency/changes_chain2reverse.html', context)


@login_required
def donate(request):
    context = {
        'title': 'Донат'
    }
    return render(request, 'currency/donate.html', context)