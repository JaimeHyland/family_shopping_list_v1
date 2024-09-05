from django.contrib import admin
from .models import ListItem, Shop, Category, Product
from django_summernote.admin import SummernoteModelAdmin

class ListItemAdmin(admin.ModelAdmin):
    # Display fields on admin/.../change page
    fields = ('product', 'default_shop', 'category', 'bought', 'cancelled')
    
    readonly_fields = ('default_shop', 'category')

    def default_shop(self, obj):
        return f"{obj.product.default_shop}"

    def category(self, obj):
        return f"{obj.product.category}"

    # Set field names for admin interface
    default_shop.short_description = 'Default Shop'
    category.short_description = 'Category'


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'slug')
    readonly_fields = ('slug','date_created',)  # the slug field read-only
    fields = ('product_name', 'slug', 'category', 'default_quantity', 'default_unit', 'default_shop', 'creator', 'date_created', 'notes', 'current')


class ShopAdmin(admin.ModelAdmin):
    list_display = ('shop_name', 'slug')
    readonly_fields = ('slug', 'date_created',)
    fields = ('shop_name', 'slug', 'type_of_shop','creator', 'date_created', 'notes', 'current')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'slug')
    readonly_fields = ('slug', 'date_created',)
    fields = ('category_name', 'slug', 'creator', 'date_created', 'notes', 'current')


admin.site.register(ListItem, ListItemAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Shop, ShopAdmin)