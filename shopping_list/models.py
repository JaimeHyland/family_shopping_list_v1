from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.

class Shop(models.Model):
    shop_name = models.CharField(max_length=50, null=False, blank=False)
    creator_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "user_who_created_shop")
    current = models.BooleanField(default=True)
    featured_image = CloudinaryField('image', default='placeholder')
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.shop_name

class Category(models.Model):
    category_name = models.CharField(max_length=50, null=False, blank=False)
    creator_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_who_created_category")
    current = models.BooleanField(default=True)
    featured_image = CloudinaryField('image', default='placeholder')
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = "categories"


class Product(models.Model):
    product_name = models.CharField(max_length=50, null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="product_category")
    default_quantity = models.IntegerField()
    default_unit = models.CharField(max_length=10)
    default_shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="default_where_to_buy")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_who_created_product")
    notes = models.TextField(null=True, blank=True)
    current = models.BooleanField(default=True)

    def __str__(self):
        return self.product_name


class List_item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_of_list_item")
    date_created = models.DateTimeField(auto_now=True)
    bought = models.BooleanField(default=False)
    date_bought = models.DateTimeField(default=None, blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_who_put_item_on_list")
    shopper = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_who_bought_item", null=True, blank=True)
    quantity_required = models.IntegerField(default=1)
    quantity_bought = models.IntegerField(default=1)
    shop_bought = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="shop_where_item_bought", null=True, blank=True)
    creator_notes = models.TextField(null=True, blank=True)
    buyer_notes = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['date_created']
        verbose_name = "list item"

    def __str__(self):
        return self.product.product_name

    def __str__(category):
        return self.product.category

