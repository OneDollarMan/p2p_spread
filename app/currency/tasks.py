import json
import threading
from time import sleep

import requests
from celery import shared_task
from django.db import connection

from currency.models import Payment, Currency, Pair, Deal, Chain2, Chain2Reverse, CurrenciesSpot, Chain3, Chain3Reverse


class DealerStealer:

    def __init__(self, pairs, thread_count):
        self.lock = threading.Lock()
        self.pairs = list(pairs)
        self.thread_count = thread_count

    def start(self):
        threads = []
        for i in range(self.thread_count):
            threads.append(threading.Thread(target=self.thread_func, name=f'stealer_thread {i}'))
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    def get_p2p_data(self, asset='USDT', fiat='RUB', trade_type='BUY', pay_types=None):
        if pay_types is None:
            pay_types = ["RaiffeisenBank"]
        headers = {'content-type': 'application/json'}
        json_data = {
            "page": 1,
            "rows": 1,
            "asset": asset,
            "fiat": fiat,
            "tradeType": trade_type,
            "payTypes": pay_types
        }
        response = requests.post('https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search', headers=headers,
                                 json=json_data)
        if response.status_code != 200:
            response.raise_for_status()
        data = json.loads(response.text)['data']
        res = []
        for row in data:
            res.append(
                {'seller': row['advertiser']['userNo'],
                 'price': row['adv']['price'],
                 'amount': row['adv']['surplusAmount'],
                 'min': row['adv']['minSingleTransAmount'],
                 'max': row['adv']['dynamicMaxSingleTransAmount']
                 }
            )
        return res

    def thread_func(self):
        while True:
            with self.lock:
                if not self.pairs:
                    break
                p = self.pairs.pop()
            deals = self.get_p2p_data(asset=p.asset.abbr, fiat=p.fiat.abbr, trade_type=p.trade_type,
                                      pay_types=[p.payment.binance_name])
            for d in deals:
                try:
                    deal = Deal.objects.get(pair=p)
                    deal.seller = d['seller']
                    deal.price = d['price']
                    deal.amount = d['amount']
                    deal.min_amount = d['min']
                    deal.max_amount = d['max']
                    deal.save()
                except Deal.DoesNotExist:
                    Deal(seller=d['seller'], price=d['price'], amount=d['amount'], min_amount=d['min'], max_amount=d['max'], pair=p).save()
            sleep(1)


@shared_task
def get_deals():
    DealerStealer(pairs=Pair.objects.all(), thread_count=10).start()
    update_chain2.delay()
    update_currencies_spot.delay()


@shared_task
def make_all_pairs():
    payments = Payment.objects.all()
    fiats = Currency.objects.filter(is_fiat=1)
    assets = Currency.objects.filter(is_fiat=0)
    Pair.objects.all().delete()
    for p in payments:
        for fiat in fiats:
            for asset in assets:
                if not Pair.objects.filter(asset=asset, fiat=fiat, payment=p, trade_type='BUY'):
                    Pair(asset=asset, fiat=fiat, payment=p, trade_type='BUY').save()
                if not Pair.objects.filter(asset=asset, fiat=fiat, payment=p, trade_type='SELL'):
                    Pair(asset=asset, fiat=fiat, payment=p, trade_type='SELL').save()


@shared_task
def calculate_chain2():
    Chain2.objects.all().delete()
    assets = Currency.objects.filter(is_fiat=0)
    fiats = Currency.objects.filter(is_fiat=1)
    for a in assets:
        for f in fiats:
            buy_pairs = Pair.objects.filter(asset=a, fiat=f, trade_type='BUY')
            sell_pairs = Pair.objects.filter(asset=a, fiat=f)
            for buy_pair in buy_pairs:
                for sell_pair in sell_pairs:
                    profit = sell_pair.price_average / buy_pair.price_average
                    try:
                        chain2 = Chain2.objects.get(buy_pair=buy_pair, sell_pair=sell_pair)
                        chain2.profit = profit
                        chain2.save()
                    except Chain2.DoesNotExist:
                        Chain2(buy_pair=buy_pair, sell_pair=sell_pair, profit=profit).save()
    calculate_chain2_reverse.delay()


@shared_task
def calculate_chain2_reverse():
    Chain2Reverse.objects.all().delete()
    c_forwards = Chain2.objects.all()
    for c_forward in c_forwards:
        c_backwards = Chain2.objects.filter(buy_pair__fiat=c_forward.sell_pair.fiat,
                                            buy_pair__payment=c_forward.sell_pair.payment,
                                            sell_pair__payment=c_forward.buy_pair.payment).exclude(pk=c_forward.pk)
        for c_backward in c_backwards:
            profit = c_backward.profit * c_forward.profit
            Chain2Reverse(forward_chain=c_forward, backward_chain=c_backward, profit=profit).save()


@shared_task
def update_chain2():
    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE currency_chain2 SET profit = (SELECT AVG(price) FROM currency_deal WHERE pair_id=sell_pair_id) / (SELECT AVG(price) FROM currency_deal WHERE pair_id=buy_pair_id)")
        cursor.execute(
            "UPDATE currency_chain2reverse SET profit = (SELECT profit FROM currency_chain2 WHERE id=backward_chain_id) * (SELECT profit FROM currency_chain2 WHERE id=forward_chain_id)")


@shared_task
def update_currencies_spot():
    for cs in CurrenciesSpot.objects.all():
        headers = {'content-type': 'application/json'}
        response = requests.get(f'https://api.binance.com/api/v3/ticker/price?symbol={cs.asset1.abbr}{cs.asset2.abbr}',
                                headers=headers)
        if response.status_code != 200:
            response.raise_for_status()
        cs.rate = float(json.loads(response.text)['price'])
        cs.save()
    update_chain3.delay()


@shared_task
def make_chain3():
    buy_pairs = Pair.objects.filter(trade_type='BUY')
    sell_pairs = Pair.objects.all()
    for buy_pair in buy_pairs:
        for sell_pair in sell_pairs:
            if buy_pair.asset != sell_pair.asset:
                try:
                    spot = CurrenciesSpot.objects.get(asset1=buy_pair.asset, asset2=sell_pair.asset)
                    profit = (sell_pair.price_average * spot.rate) / buy_pair.price_average
                except CurrenciesSpot.DoesNotExist:
                    spot = CurrenciesSpot.objects.get(asset1=sell_pair.asset, asset2=buy_pair.asset)
                    profit = sell_pair.price_average / (buy_pair.price_average * spot.rate)
                try:
                    chain3 = Chain3.objects.get(buy_pair=buy_pair, sell_pair=sell_pair, spot=spot)
                    chain3.profit = profit
                    chain3.save()
                except Chain3.DoesNotExist:
                    Chain3(buy_pair=buy_pair, sell_pair=sell_pair, profit=profit, spot=spot).save()


@shared_task
def update_chain3():
    for chain3 in Chain3.objects.all():
        if chain3.buy_pair.asset == chain3.spot.asset1:
            chain3.profit = (chain3.sell_pair.price_average * chain3.spot.rate) / chain3.buy_pair.price_average
        else:
            chain3.profit = chain3.sell_pair.price_average / (chain3.buy_pair.price_average * chain3.spot.rate)
        chain3.save()
    update_chain3_reverse.delay()


@shared_task
def make_chain3_reverse():
    Chain3Reverse.objects.all().delete()
    c_forwards = Chain3.objects.all()
    for c_forward in c_forwards:
        c_backwards = Chain3.objects.filter(buy_pair__fiat=c_forward.sell_pair.fiat,
                                            buy_pair__payment=c_forward.sell_pair.payment,
                                            sell_pair__payment=c_forward.buy_pair.payment).exclude(pk=c_forward.pk)
        for c_backward in c_backwards:
            profit = c_backward.profit * c_forward.profit
            Chain3Reverse(forward_chain=c_forward, backward_chain=c_backward, profit=profit).save()


@shared_task
def update_chain3_reverse():
    with connection.cursor() as cursor:
        cursor.execute("UPDATE currency_chain3reverse SET profit = (SELECT profit FROM currency_chain3 WHERE id=backward_chain_id) * (SELECT profit FROM currency_chain3 WHERE id=forward_chain_id)")
