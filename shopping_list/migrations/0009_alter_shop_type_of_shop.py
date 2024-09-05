# Generated by Django 4.2.7 on 2024-09-05 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping_list', '0008_shop_type_of_shop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='type_of_shop',
            field=models.IntegerField(choices=[(1, 'Supermarket'), (2, 'Organic shop'), (3, 'DIY center'), (4, 'Drugstore'), (5, 'Specialist retailer'), (6, 'Stationer')]),
        ),
    ]
