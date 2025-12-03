from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('quotes/', views.quote_list, name='quote_list'),
    path('quotes/new/', views.quote_create, name='quote_create'),
    path('quotes/<int:pk>/delete/', views.quote_delete, name='quote_delete'),
    path('health/', views.health, name='health'),
]
