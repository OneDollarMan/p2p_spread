from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('rates', views.rates, name='rates'),
    path('changes', views.changes, name='changes'),
    path('donate', views.donate, name='donate')
]
