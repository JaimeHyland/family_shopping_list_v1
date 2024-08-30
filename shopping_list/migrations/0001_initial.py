# Generated by Django 5.1 on 2024-08-30 07:08

import cloudinary.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50)),
                ('current', models.BooleanField(default=True)),
                ('featured_image', cloudinary.models.CloudinaryField(default='placeholder', max_length=255, verbose_name='image')),
                ('notes', models.TextField(blank=True, null=True)),
                ('creator_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_who_created_category', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_name', models.CharField(max_length=50)),
                ('current', models.BooleanField(default=True)),
                ('featured_image', cloudinary.models.CloudinaryField(default='placeholder', max_length=255, verbose_name='image')),
                ('notes', models.TextField(blank=True, null=True)),
                ('creator_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_who_created_shop', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=50)),
                ('default_quantity', models.IntegerField()),
                ('default_unit', models.CharField(max_length=10)),
                ('notes', models.TextField(blank=True, null=True)),
                ('current', models.BooleanField(default=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_category', to='shopping_list.category')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_who_created_product', to=settings.AUTH_USER_MODEL)),
                ('default_shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='default_where_to_buy', to='shopping_list.shop')),
            ],
        ),
        migrations.CreateModel(
            name='List_item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('bought', models.BooleanField(default=False)),
                ('date_bought', models.DateTimeField(blank=True, default=None, null=True)),
                ('quantity_required', models.IntegerField(default=1)),
                ('quantity_bought', models.IntegerField(default=1)),
                ('creator_notes', models.TextField(blank=True, null=True)),
                ('buyer_notes', models.TextField(blank=True, null=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_who_put_item_on_list', to=settings.AUTH_USER_MODEL)),
                ('shopper', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_who_bought_item', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_of_list_item', to='shopping_list.product')),
                ('shop_bought', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_where_item_bought', to='shopping_list.shop')),
            ],
            options={
                'ordering': ['date_created'],
            },
        ),
    ]
