from . import views
from django.urls import path



urlpatterns = [
    path('', views.ShoppingListView.as_view(), name='shopping_list'),
    path('list-item-<slug:slug>/', views.ListItemView.as_view(), name='list_item'),
    path('add-to-shopping-list/', views.AddToShoppingListView.as_view(), name='add_to_shopping_list'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/<slug:slug>/', views.ProductView.as_view(), name='product_detail'),
    path('add-product/', views.AddProductView.as_view(), name='add_product'),
    path('shops/', views.ShopListView.as_view(), name='shop_list'),
    path('shops/<slug:slug>/', views.ShopView.as_view(), name='shop_detail'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/<slug:slug>/', views.CategoryView.as_view(), name='category_detail'),
]