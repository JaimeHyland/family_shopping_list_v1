from django.core.management.base import BaseCommand
from django.utils.text import slugify
from shopping_list.models import Shop


class Command(BaseCommand):
    help = 'Generate slugs for shops without them'

    def handle(self, *args, **kwargs):
        unslugged_shops = Shop.objects.filter(slug__isnull=True)
        for shop in unslugged_shops:
            shop.slug = slugify(shop.shop_name)
            shop.save()

        self.stdout.write(self.style.SUCCESS(f"Updated slugs for {unslugged_shops.count()} shops."))
