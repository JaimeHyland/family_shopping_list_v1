from django.contrib import admin
from .models import List_item, Shop, Category, Product
from django_summernote.admin import SummernoteModelAdmin

@admin.register(List_item, Shop, Category, Product)
class NoteAdmin(SummernoteModelAdmin):

    summernote_fields = ('creator_notes', 'shopper_notes')
    search_fields = ['product']