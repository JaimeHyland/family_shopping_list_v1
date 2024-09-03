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

admin.site.register(ListItem, ListItemAdmin)
