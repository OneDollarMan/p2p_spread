from currency.models import Chain2, Pair, Chain2Reverse


def get_chain2_objects_filtered(form=None):
    if form is None:
        return Chain2.objects.filter(buy_pair__fiat__abbr='RUB').order_by('-profit')[:20]
    else:
        asset = form['currency'].value()
        buy_payment = form['buy_payment'].value()
        sell_payment = form['sell_payment'].value()
        is_sell_orders = form['is_sell_orders'].value()
        objects = Chain2.objects.filter(buy_pair__fiat__abbr='RUB')
        try:
            if asset:
                objects = objects.filter(buy_pair__asset_id=int(asset))
            if buy_payment:
                objects = objects.filter(buy_pair__payment_id=int(buy_payment))
            if sell_payment:
                objects = objects.filter(sell_pair__payment_id=int(sell_payment))
            if is_sell_orders:
                objects = objects.filter(sell_pair__trade_type=Pair.TradeType.SELL)
        except ValueError:
            return None
        return objects.order_by('-profit')[:20]


def get_chain2reverse_objects_filtered(form=None):
    if form is None:
        return Chain2Reverse.objects.filter(forward_chain__buy_pair__fiat__abbr='RUB').order_by('-profit')[:20]
    else:
        buy_payment = form['buy_payment'].value()
        sell_payment = form['sell_payment'].value()
        is_sell_orders = form['is_sell_orders'].value()
        objects = Chain2Reverse.objects.filter(forward_chain__buy_pair__fiat__abbr='RUB')
        try:
            if buy_payment:
                objects = objects.filter(forward_chain__buy_pair__payment_id=int(buy_payment))
            if sell_payment:
                objects = objects.filter(forward_chain__sell_pair__payment_id=int(sell_payment))
            if is_sell_orders:
                objects = objects.filter(forward_chain__sell_pair__trade_type=Pair.TradeType.SELL)
                objects = objects.filter(backward_chain__sell_pair__trade_type=Pair.TradeType.SELL)
        except ValueError:
            return None
        return objects.order_by('-profit')[:20]
