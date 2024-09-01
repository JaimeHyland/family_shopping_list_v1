from django.urls import path

from . import views


urlpatterns = [
    path('', views.shopping_list, name='shopping_list'),
    path('shop/<str:shop_name>/', views.shop, name='shop'),
]