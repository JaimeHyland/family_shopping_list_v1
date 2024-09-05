from django.shortcuts import render, redirect, get_object_or_404
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.views import View
from .models import ListItem, Product, Shop, Category
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from collections import defaultdict


def shop(request, shop_name):
    context = {"shop_name": shop_name}
    return render(request, "shopping_list/shop.html", context)

def get(self, request, *args, **kwargs):
        try:
            items = ListItem.objects.filter(bought=False)
            print(f"Debug: {items}")
            return render(request, 'shopping_list/shopping_list.html', {'items': items})

        except Exception as e:
            print(f"Error processing GET request: {e}")
            return HttpResponseBadRequest("Invalid request")

def mark_item(request, item_id, status):
    list_item = get_object_or_404(ListItem, id=item_id)
    list_item.status = status
    list_item.save()

    # Send update to WebSocket group
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "shopping_list_updates",
        {
            'type': 'list_item_update',
            'list_item_id': list_item.id,
            'status': status,
            'user': request.user.username
        }
    )

    return redirect('shopping_list')

@method_decorator(login_required, name='dispatch')
class ShoppingListView(View):
    def get(self, request, *args, **kwargs):
        shopping_list = ListItem.objects.filter(bought=False, cancelled=False).order_by('id')
        return render(request, 'shopping_list/shopping_list.html', {'shopping_list': shopping_list})

    def post(self, request, *args, **kwargs):
        try:
            
            item_id = request.POST.get('item_id')
            action = request.POST.get('action')

            if not item_id or not action:
                print("Bugfix: Invalid request: Missing item_id or action")
                return HttpResponseBadRequest("Invalid request: Missing item_id or action")

            item = get_object_or_404(ListItem, id=item_id)

            if action == 'cancel':
                item.cancelled = True
            elif action == 'uncancel':
                item.cancelled = False
            elif action == 'buy':
                item.bought = True
            elif action == 'unbuy':
                item.bought = False
            else:
                return HttpResponseBadRequest("Invalid request: Unknown action")

            item.save()
            return redirect('shopping_list')

        except Exception as e:
            print(f"Error processing POST request: {e}")
            return HttpResponseBadRequest("Invalid request")


class ListItemView(View):
    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        listItem = get_object_or_404(ListItem, product__slug=slug)
        return render(request, 'shopping_list/list_item.html', {'list_item': listItem})


class ProductListView(View):
    def get(self, request, *args, **kwargs):
        product_list = Product.objects.filter(current=True).order_by('category__category_name', 'date_created')
        
        grouped_products = {}

        # Group products by category
        for product in product_list:
            category_name = product.category.category_name
            if category_name not in grouped_products:
                grouped_products[category_name] = []
            grouped_products[category_name].append(product)

        print("DEBUG! Grouped Products:", grouped_products)
        return render(request, 'shopping_list/product_list.html', {'grouped_products': grouped_products})


class ShopListView(View):
    def get(self, request, *args, **kwargs):
        shopList = Shop.objects.filter(current=True)
        return render(request, 'shopping_list/shop_list.html', {'shop_list': shopList})

class CategoryListView(View):
    def get(self, request, *args, **kwargs):
        categoryList = Category.objects.filter(current=True)
        return render(request, 'shopping_list/category_list.html', {'category_list': categoryList})

class ProductView(View):
    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        product = get_object_or_404(Product, slug=slug)
        return render(request, 'shopping_list/product.html', {'product': product})

class ShopView(View):
    def get(self, request, *args, **kwargs):
        shop = get_object_or_404(Shop, slug=slug)
        return render(request, 'shopping_list/shop.html', {'shop': shop})

class CategoryView(View):
    def get(self, request, *args, **kwargs):
        category = get_object_or_404(Category, slug=slug)
        return render(request, 'shopping_list/category.html', {'category': category})


class AddToShoppingListView(View):
    def post(self, request, *args, **kwargs):
        selected_products = request.POST.getlist('selected_products')
        creator = request.user

        for product_id in selected_products:
            product = Product.objects.get(id=product_id)
            ListItem.objects.create(product=product, quantity_required=1, creator=creator)

        return redirect('shopping_list')
