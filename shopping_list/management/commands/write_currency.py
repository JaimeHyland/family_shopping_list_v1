from django.core.management.base import BaseCommand
from shopping_list.models import Product, Category, Shop

class Command(BaseCommand):
    help = 'Set products, list items, shops and categories with null value for current to True'

    def handle(self, *args, **kwargs):
        null_current_products = Product.objects.filter(current__isnull=True)
        for product in null_current_products:
            product.current = True
            product.save()
        
        self.stdout.write(self.style.SUCCESS(f"Updated slugs for {null_current_products.count()} products."))

        null_current_categories = Category.objects.filter(current__isnull=True)
        for category in null_current_categories:
            category.current = True
            category.save()
        
        self.stdout.write(self.style.SUCCESS(f"Updated slugs for {null_current_categories.count()} categories."))

        null_current_shops = Shop.objects.filter(current__isnull=True)
        for shop in null_current_categories:
            shop.current = True
            shop.save()
        
        self.stdout.write(self.style.SUCCESS(f"Updated slugs for {null_current_categories.count()} shops."))