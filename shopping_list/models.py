from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from cloudinary.models import CloudinaryField

# Create your models here.

class Shop(models.Model):
    shop_name = models.CharField(max_length=50, null=False, blank=False)
    slug = models.SlugField(max_length = 250, unique=True, null = True, blank = True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "user_who_created_shop")
    date_created = models.DateTimeField(auto_now=True)
    notes = models.TextField(null=True, blank=True)
    current = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.shop_name)
            slug = base_slug
            count = 1
            while Shop.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{count}'
                count += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.shop_name

class Category(models.Model):
    category_name = models.CharField(max_length=50, null=False, blank=False)
    slug = models.SlugField(max_length = 250, unique=True, null = True, blank = True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_who_created_category")
    date_created = models.DateTimeField(auto_now=True)
    notes = models.TextField(null=True, blank=True)
    current = models.BooleanField(default=True)
    

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.category_name)
            slug = base_slug
            count = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{count}'
                count += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        ordering = ['date_created']
        return self.category_name

    class Meta:
        verbose_name_plural = "categories"


class Product(models.Model):
    product_name = models.CharField(max_length=254, null=False, blank=False)
    slug = models.SlugField(max_length = 250, unique=True, null = True, blank = True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="product_category")
    default_quantity = models.IntegerField(null=True, blank=True)
    default_unit = models.CharField(max_length=32, null=True, blank=True)
    default_shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="default_where_to_buy")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_who_created_product")
    date_created = models.DateTimeField(auto_now=True)
    notes = models.TextField(null=True, blank=True)
    current = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.product_name)
            slug = base_slug
            count = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{count}'
                count += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product_name

    class Meta:
        ordering = ['date_created']


class ListItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_of_list_item")
    date_created = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_who_put_item_on_list")
    bought = models.BooleanField(default=False)
    date_bought = models.DateTimeField(default=None, blank=True, null=True)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_who_bought_item", null=True, blank=True)
    cancelled = models.BooleanField(default=False)
    date_cancelled = models.DateTimeField(default=None, blank=True, null=True)
    cancelled_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_who_cancelled_item", null=True, blank=True)
    quantity_required = models.IntegerField(default=1)
    quantity_bought = models.IntegerField(default=0)
    shop_bought = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="shop_where_item_bought", null=True, blank=True)
    creator_notes = models.TextField(null=True, blank=True)
    shopper_notes = models.TextField(null=True, blank=True)
    

    class Meta:
        ordering = ['date_created']
        verbose_name = "list item"

    def __str__(self):
        return f"{self.product.product_name} {self.product.category} ({self.product.default_shop})"
