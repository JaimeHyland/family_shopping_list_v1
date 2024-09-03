from django.shortcuts import render
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.views import View
from .models import ListItem
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


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

    def product_detail(request, slug):
        product = get_object_or_404(Product, slug=slug)
        return render(request, 'shopping_list/product_detail.html', {'product': product})