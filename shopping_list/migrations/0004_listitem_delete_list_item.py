# Generated by Django 4.2.7 on 2024-09-02 10:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shopping_list', '0003_alter_product_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('bought', models.BooleanField(default=False)),
                ('date_bought', models.DateTimeField(blank=True, default=None, null=True)),
                ('quantity_required', models.IntegerField(default=1)),
                ('quantity_bought', models.IntegerField(default=0)),
                ('creator_notes', models.TextField(blank=True, null=True)),
                ('shopper_notes', models.TextField(blank=True, null=True)),
                ('current', models.BooleanField(default=True)),
                ('date_cancelled', models.DateTimeField(blank=True, default=None, null=True)),
                ('buyer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_who_bought_item', to=settings.AUTH_USER_MODEL)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_who_put_item_on_list', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_of_list_item', to='shopping_list.product')),
                ('shop_bought', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_where_item_bought', to='shopping_list.shop')),
            ],
            options={
                'verbose_name': 'list item',
                'ordering': ['date_created'],
            },
        ),
        migrations.DeleteModel(
            name='List_item',
        ),
    ]
