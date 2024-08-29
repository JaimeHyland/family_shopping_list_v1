from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('shop/<str:shop_name>/', views.shop, name='shop'),
]