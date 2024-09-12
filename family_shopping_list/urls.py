"""
URL configuration for family_shopping_list project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from shopping_list import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('welcome_page/', views.welcome_page, name='logged_out_homepage'),
    path('', include('shopping_list.urls')),
    path("accounts/", include("allauth.urls")),
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(), name='account_change_password'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
]
