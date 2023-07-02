from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('rates', views.rates, name='rates'),
    path('changes/chain2', views.changes_chain2, name='changes_chain2'),
    path('changes/chain2reverse', views.changes_chain2reverse, name='changes_chain2reverse'),
    path('donate', views.donate, name='donate')
]
