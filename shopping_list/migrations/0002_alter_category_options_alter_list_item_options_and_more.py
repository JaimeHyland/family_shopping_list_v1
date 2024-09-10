# Generated by Django 4.2.7 on 2024-08-31 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping_list', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categories'},
        ),
        migrations.AlterModelOptions(
            name='list_item',
            options={'ordering': ['date_created'], 'verbose_name': 'list item'},
        ),
        migrations.RenameField(
            model_name='list_item',
            old_name='shopper',
            new_name='buyer',
        ),
        migrations.RenameField(
            model_name='list_item',
            old_name='buyer_notes',
            new_name='shopper_notes',
        ),
        migrations.RenameField(
            model_name='shop',
            old_name='creator_id',
            new_name='creator',
        ),
        migrations.RemoveField(
            model_name='category',
            name='featured_image',
        ),
        migrations.RemoveField(
            model_name='shop',
            name='featured_image',
        ),
        migrations.AddField(
            model_name='list_item',
            name='current',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='list_item',
            name='date_cancelled',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='default_quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='default_unit',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_name',
            field=models.CharField(max_length=254),
        ),
    ]