import json
import threading
from time import sleep

import requests
from celery import shared_task

from currency.models import Payment, Currency, Pair, Deal, Chain2


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
                 'amount': row['adv']['surplusAmount']
                 }
            )
        return res

    def thread_func(self):
        while True:
            with self.lock:
                if not self.pairs:
                    break
                p = self.pairs.pop()
            deals = self.get_p2p_data(asset=p.asset.abbr, fiat=p.fiat.abbr, trade_type=p.trade_type, pay_types=[p.payment.binance_name])
            for d in deals:
                Deal(seller=d['seller'], price=d['price'], amount=d['amount'], pair=p).save()
            sleep(1)


@shared_task
def get_deals():
    Deal.objects.all().delete()
    DealerStealer(pairs=Pair.objects.all(), thread_count=10).start()
    calculate_profit.delay()


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
def calculate_profit():
    assets = Currency.objects.filter(is_fiat=0)
    fiats = Currency.objects.filter(is_fiat=1)
    Chain2.objects.all().delete()
    for a in assets:
        for f in fiats:
            buy_pairs = Pair.objects.filter(asset=a, fiat=f, trade_type='BUY')
            sell_pairs = Pair.objects.filter(asset=a, fiat=f)
            for buy_pair in buy_pairs:
                try:
                    buy_deal = Deal.objects.get(pair=buy_pair)
                except Deal.DoesNotExist:
                    continue
                for sell_pair in sell_pairs:
                    try:
                        sell_deal = Deal.objects.get(pair=sell_pair)
                    except Deal.DoesNotExist:
                        continue
                    profit = round((sell_deal.price / buy_deal.price) * 100 - 100, 2)
                    Chain2(buy_pair=buy_pair, buy_price=buy_deal.price, sell_pair=sell_pair, sell_price=sell_deal.price, profit=profit).save()
