import json
import requests
from currency.models import Payment, Currency, Pair, Deal


def get_p2p_data(asset='USDT', fiat='RUB', trade_type='BUY', pay_types=None):
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


def get_deals():
    Deal.objects.all().delete()
    for p in Pair.objects.all():
        deals = get_p2p_data(asset=p.asset.abbr, fiat=p.fiat.abbr, trade_type=p.trade_type, pay_types=[p.payment.binance_name])
        for d in deals:
            Deal(seller=d['seller'], price=d['price'], amount=d['amount'], pair=p).save()
        print('saved deals for pair:' + str(p))


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
