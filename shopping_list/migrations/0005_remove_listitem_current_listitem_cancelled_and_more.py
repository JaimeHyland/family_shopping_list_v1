# Generated by Django 4.2.7 on 2024-09-02 11:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shopping_list', '0004_listitem_delete_list_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listitem',
            name='current',
        ),
        migrations.AddField(
            model_name='listitem',
            name='cancelled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='listitem',
            name='cancelled_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_who_cancelled_item', to=settings.AUTH_USER_MODEL),
        ),
    ]
