from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.

class Shop(models.Model):
    shop_name = models.CharField(max_length=50, null=False, blank=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "user_who_created_shop")
    date_created = models.DateTimeField(auto_now=True)
    notes = models.TextField(null=True, blank=True)
    current = models.BooleanField(default=True)

    def __str__(self):
        return self.shop_name

class Category(models.Model):
    category_name = models.CharField(max_length=50, null=False, blank=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_who_created_category")
    date_created = models.DateTimeField(auto_now=True)
    notes = models.TextField(null=True, blank=True)
    current = models.BooleanField(default=True)
    

    def __str__(self):
        ordering = ['date_created']
        return self.category_name

    class Meta:
        verbose_name_plural = "categories"


class Product(models.Model):
    product_name = models.CharField(max_length=254, null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="product_category")
    default_quantity = models.IntegerField(null=True, blank=True)
    default_unit = models.CharField(max_length=32, null=True, blank=True)
    default_shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="default_where_to_buy")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_who_created_product")
    date_created = models.DateTimeField(auto_now=True)
    notes = models.TextField(null=True, blank=True)
    current = models.BooleanField(default=True)

    def __str__(self):
        return self.product_name

    class Meta:
        ordering = ['date_created']


class List_item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_of_list_item")
    date_created = models.DateTimeField(auto_now=True)
    bought = models.BooleanField(default=False)
    date_bought = models.DateTimeField(default=None, blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_who_put_item_on_list")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_who_bought_item", null=True, blank=True)
    quantity_required = models.IntegerField(default=1)
    quantity_bought = models.IntegerField(default=1)
    shop_bought = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="shop_where_item_bought", null=True, blank=True)
    creator_notes = models.TextField(null=True, blank=True)
    shopper_notes = models.TextField(null=True, blank=True)
    current = models.BooleanField(default=True)
    date_cancelled = models.DateTimeField(default=None, blank=True, null=True)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_who_bought_item", null=True, blank=True)

    class Meta:
        ordering = ['date_created']
        verbose_name = "list item"

    def __str__(self):
        return self.product.product_name

    def __str__(category):
        return self.product.category

    def __str__(default_shop):
        return self.product.default_shop

