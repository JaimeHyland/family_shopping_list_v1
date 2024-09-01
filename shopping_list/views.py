from django.shortcuts import render

def shopping_list(request):
    return render(request, "shopping_list/shopping_list.html")

def shop(request, shop_name):
    context = {"shop_name": shop_name}
    return render(request, "shopping_list/shop.html", context)