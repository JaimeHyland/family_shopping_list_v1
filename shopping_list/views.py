
from .models import ListItem, Product, Shop, Category
from .forms import ProductForm, ShopForm, CategoryForm
from utilities.utils import is_adult

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from allauth.account.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin


def welcome_page(request):
    if request.user.is_authenticated:
        return redirect('shopping_list')
    return render(request, 'logged_out_homepage.html')


@login_required
def shop(request, shop_name):
    context = {"shop_name": shop_name}
    return render(request, "shopping_list/shop.html", context)


@login_required
def get(self, request, *args, **kwargs):
        try:
            items = ListItem.objects.filter(bought=False)
            return render(request, 'shopping_list/shopping_list.html', {'items': items})

        except Exception as e:
            print(f"Error processing GET request: {e}")
            return HttpResponseBadRequest("Invalid request")


@login_required
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

class AdultRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return is_adult(self.request.user)

@method_decorator(login_required, name='dispatch')
class ShoppingListView(View):
    def get(self, request, *args, **kwargs):
        filter_chosen = request.GET.get('filter_by', 'category')  # Both options are 'category' by default
        order_chosen = request.GET.get('order_by', 'category')

        shopping_list = ListItem.objects.filter(bought=False, cancelled=False, current=True)
        
        if filter_chosen == 'shop':
            shopping_list = shopping_list.order_by('shop_bought__shop_name')
        elif filter_chosen == 'category':
            shopping_list = shopping_list.order_by('product__category__category_name')

        if order_chosen == 'shop':
            shopping_list = shopping_list.order_by('shop_bought__shop_name', 'product__category__category_name')
        elif order_chosen == 'category':
            shopping_list = shopping_list.order_by('product__category__category_name', 'shop_bought__shop_name')

        shopping_list = ListItem.objects.filter(current=True, bought=False, cancelled=False).order_by('id')
        shops = Shop.objects.filter(current=True).order_by('type_of_shop')
        return render(request, 'shopping_list/shopping_list.html', {
            'shopping_list': shopping_list,
            'shops': shops,
            'filter_chosen': filter_chosen,
            'order_chosen': order_chosen,
            })

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


@method_decorator(login_required, name='dispatch')
class ListItemView(View):
    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        listItem = get_object_or_404(ListItem, product__slug=slug, current=True, bought=False)
        return render(request, 'shopping_list/list_item.html', {'list_item': listItem})


@method_decorator(login_required, name='dispatch')
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
        # For the AddProductModalDialog to populate the dropdowns
        categories = Category.objects.all()
        shops = Shop.objects.all()

        return render(request, 'shopping_list/product_list.html', {
            'grouped_products': grouped_products,
            'categories': categories,
            'shops': shops
        })


@method_decorator(login_required, name='dispatch')
class ShopListView(View):
    def get(self, request, *args, **kwargs):
        shopList = Shop.objects.filter(current=True)
        types_of_shop = Shop.TYPES_OF_SHOP
        return render(request, 'shopping_list/shop_list.html', {'shop_list': shopList, 'types_of_shop': types_of_shop})


@method_decorator(login_required, name='dispatch')
class CategoryListView(View):
    def get(self, request, *args, **kwargs):
        categoryList = Category.objects.filter(current=True)
        return render(request, 'shopping_list/category_list.html', {'category_list': categoryList})


@method_decorator(login_required, name='dispatch')
class ProductView(View):
    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        product = get_object_or_404(Product, slug=slug)
        form = ProductForm(instance=product)
        return render(request, 'shopping_list/product.html', {'form': form, 'product': product})

    def post(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        product = get_object_or_404(Product, slug=slug)
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
        else:
            messages.error(request, "A product with this name already exists.")
        return render(request, 'shopping_list/product.html', {'form': form, 'product': product})


@method_decorator(login_required, name='dispatch')
class ShopView(View):
    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        shop = get_object_or_404(Shop, slug=slug)
        form = ShopForm(instance=shop)
        return render(request, 'shopping_list/shop.html', {'form': form, 'shop': shop})

    def post(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        shop = get_object_or_404(Shop, slug=slug)
        form = ShopForm(request.POST, instance=shop)
        if form.is_valid():
            form.save()
            return redirect('shop_list')
        else:
            for field, errors in form.errors.items():
                print(f"{field}: {errors}")
        return render(request, 'shopping_list/shop.html', {'form': form, 'shop': shop})


@method_decorator(login_required, name='dispatch')
class CategoryView(View):
    def get(self, request, *args, **kwargs):
        category = get_object_or_404(Category, slug=slug)
        return render(request, 'shopping_list/category.html', {'category': category})


@method_decorator(login_required, name='dispatch')
class AddToShoppingListView(View):
    def post(self, request, *args, **kwargs):
        selected_products = request.POST.getlist('selected-products')
        creator = request.user

        for product_id in selected_products:
            product = Product.objects.get(id=product_id)
            ListItem.objects.create(product=product, quantity_required=1, creator=creator)
        
        return redirect('shopping_list')


@method_decorator(login_required, name='dispatch')
class AddProductView(View):
    def post(self, request, *args, **kwargs):
        product_name = request.POST.get('product_name')
        category_id = request.POST.get('category')
        default_shop_id = request.POST.get('default_shop')

        category = Category.objects.get(id=category_id)
        default_shop = Shop.objects.get(id=default_shop_id)

        Product.objects.create(
            product_name=product_name,
            category=category,
            default_shop=default_shop
        )

        return redirect('product_list')

@method_decorator(login_required, name='dispatch')
class AddShopView(View):
    def post(self, request, *args, **kwargs):
        shop_name = request.POST.get('shop_name')
        type_of_shop = request.POST.get('type_of_shop')
        notes = request.POST.get('notes')

        Shop.objects.create(
            shop_name=shop_name,
            type_of_shop=type_of_shop,
            notes=notes,
        )

        return redirect('shop_list')

@method_decorator(login_required, name='dispatch')
class AddCategoryView(View):
    def post(self, request, *args, **kwargs):
        category_name = request.POST.get('category_name')
        notes = request.POST.get('notes')

        Category.objects.create(
            category_name=category_name,
            notes=notes,
        )

        return redirect('category_list')
