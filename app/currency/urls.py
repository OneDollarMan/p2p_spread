from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('rates', views.rates, name='rates'),
    path('changes/chain2', views.changes_chain2, name='changes_chain2'),
    path('changes/chain2reverse', views.changes_chain2reverse, name='changes_chain2reverse'),
    path('changes/chain3', views.changes_chain3, name='changes_chain3'),
    path('changes/chain3reverse', views.changes_chain3reverse, name='changes_chain3reverse'),
    path('donate', views.donate, name='donate')
]
