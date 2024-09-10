# Generated by Django 4.2.7 on 2024-09-05 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping_list', '0007_category_slug_shop_slug_alter_product_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='type_of_shop',
            field=models.IntegerField(choices=[(1, 'Supermarket'), (2, 'Organic shop'), (3, 'DIY center'), (4, 'Drugstore'), (5, 'Specialist retailer')], default=1),
            preserve_default=False,
        ),
    ]