from django import forms
from currency.models import Currency, Payment


class Chain2Form(forms.Form):
    currency = forms.ModelChoiceField(queryset=Currency.objects.filter(is_fiat=0), label='Актив', required=False)
    buy_payment = forms.ModelChoiceField(queryset=Payment.objects.all(), label='Способ оплаты при покупке', required=False)
    sell_payment = forms.ModelChoiceField(queryset=Payment.objects.all(), label='Способ оплаты при продаже', required=False)
    is_sell_orders = forms.BooleanField(label='Без продаж заявкой', required=False)


class Chain2ReverseForm(forms.Form):
    buy_payment = forms.ModelChoiceField(queryset=Payment.objects.all(), label='Способ оплаты при покупке', required=False)
    sell_payment = forms.ModelChoiceField(queryset=Payment.objects.all(), label='Способ оплаты при продаже', required=False)
    is_sell_orders = forms.BooleanField(label='Без продаж заявкой', required=False)

