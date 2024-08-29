from django.shortcuts import render

def index(request):
    return render(request, "shopping_list/index.html")

def shop(request, shop_name):
    context = {"shop_name": shop_name}
    return render(request, "shopping_list/shop.html", context)