from django.contrib import admin
from .models import ListItem, Shop, Category, Product
from django_summernote.admin import SummernoteModelAdmin

class ListItemAdmin(admin.ModelAdmin):
    # Display fields on admin/.../change page
    fields = ('product', 'category', 'preferred_shop', 'bought', 'buyer', 'shop_bought', 'date_bought', 'creator_notes', 'shopper_notes', 'cancelled', 'cancelled_by', 'date_cancelled', 'quantity_required', 'quantity_bought', 'current', 'date_created', 'creator')

    readonly_fields = ('default_shop', 'category', 'creator',)

    def default_shop(self, obj):
        return f"{obj.product.default_shop}"

    def category(self, obj):
        return f"{obj.product.category}"

    default_shop.short_description = 'Default Shop'
    category.short_description = 'Category'


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'slug')
    fields = ('product_name', 'slug', 'category', 'default_quantity', 'default_unit', 'default_shop', 'creator', 'date_created', 'notes', 'current',)
    readonly_fields = ('slug','date_created', 'creator',)


class ShopAdmin(admin.ModelAdmin):
    list_display = ('shop_name', 'slug')
    fields = ('shop_name', 'slug', 'type_of_shop','creator', 'date_created', 'notes', 'current',)
    readonly_fields = ('slug', 'date_created', 'creator',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'slug')
    fields = ('category_name', 'slug', 'creator', 'date_created', 'notes', 'current',)
    readonly_fields = ('slug', 'date_created','creator',)


admin.site.register(ListItem, ListItemAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Shop, ShopAdmin)