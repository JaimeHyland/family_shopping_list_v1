from django.contrib import admin
from .models import List_item, Shop, Category, Product
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Shop, Category, Product, List_item)
class NoteAdmin(SummernoteModelAdmin):

    summernote_fields = ('creator_notes', 'buyer_notes')
    search_fields = ['product_name']