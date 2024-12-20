# Generated by Django 5.1.3 on 2024-11-13 08:33

from django.db import migrations
from django.utils.text import slugify

def populate_slugs(apps, schema_editor):
    ListItem = apps.get_model('shopping_list', 'ListItem')
    for item in ListItem.objects.all():
        if not item.slug:
            item.slug = slugify(f"{item.product.slug}-{item.id}")
            item.save(update_fields=['slug'])

class Migration(migrations.Migration):

    dependencies = [
        ('shopping_list', '0016_listitem_slug'),
    ]

    operations = [
        migrations.RunPython(populate_slugs),
    ]
