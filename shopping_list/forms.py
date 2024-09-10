from django import forms
from .models import Product, Shop, Category
from django.core.exceptions import ValidationError


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'category', 'default_quantity', 'default_unit', 'default_shop', 'notes']

    def clean_product_name(self):
        product_name = self.cleaned_data.get('product_name')
        if product_name:
            normalized_name = product_name.lower()
            if self.instance.pk:
                # Existing product: Check case-insensitively except itself
                if Product.objects.exclude(pk=self.instance.pk).filter(
                    product_name__iexact=normalized_name,
                    current=True
                ).exists():
                    raise ValidationError("A product with this name already exists and is marked as current.")
            else:
                # New product: Check case-insensitively
                if Product.objects.filter(
                    product_name__iexact=normalized_name,
                    current=True
                ).exists():
                    raise ValidationError("A product with this name already exists and is marked as current.")
        return product_name


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['shop_name', 'type_of_shop', 'notes',]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'notes',]
