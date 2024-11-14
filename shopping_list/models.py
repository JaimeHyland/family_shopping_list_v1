from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.exceptions import ValidationError


class Shop(models.Model):

    TYPES_OF_SHOP = (
        (1, 'Supermarket'),
        (2, 'Organic shop'),
        (3, 'DIY center'),
        (4, 'Drugstore'),
        (5, 'Stationer'),
        (6, 'Specialist retailer'),
        (7, 'Flatpack furniture'),
        (8, 'Deli & fine foods'),
        (9, 'Wines and spirits'),
    )

    shop_name = models.CharField(max_length=50, null=False, blank=False)
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True,
        related_name="user_who_created_shop"
    )
    date_created = models.DateTimeField(auto_now=True)
    notes = models.TextField(null=True, blank=True)
    type_of_shop = models.IntegerField(choices=TYPES_OF_SHOP)
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
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="user_who_created_category"
        )
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
        return self.category_name

    class Meta:
        verbose_name_plural = "categories"


class Product(models.Model):
    product_name = models.CharField(max_length=254, null=False, blank=False)
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="product_category"
    )
    default_quantity = models.IntegerField(null=True, blank=True)
    default_unit = models.CharField(max_length=32, null=True, blank=True)
    default_shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, related_name="default_where_to_buy"
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="user_who_created_product"
    )
    date_created = models.DateTimeField(auto_now=True)
    notes = models.TextField(null=True, blank=True)
    current = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            # New instance
            base_slug = slugify(self.product_name)
            slug = base_slug
            count = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{count}'
                count += 1
            self.slug = slug
        else:
            # Existing instance
            old_product = Product.objects.get(pk=self.pk)
            if old_product.product_name != self.product_name:
                base_slug = slugify(self.product_name)
                slug = base_slug
                count = 1
                while Product.objects.filter(slug=slug).exists():
                    slug = f'{base_slug}-{count}'
                    count += 1
                self.slug = slug

        super().save(*args, **kwargs)

    def clean(self):
        # Normalize product name to lowercase
        lc_name = self.product_name.lower()

        if self.pk:
            # Existing product: Check for duplicates case-insensitively
            if Product.objects.exclude(pk=self.pk).filter(
                product_name__iexact=lc_name,
                current=True
            ).exists():
                raise ValidationError(
                    'A product with this name already exists.'
                )
        else:
            # New product: Check for duplicates case-insensitively
            if Product.objects.filter(
                product_name__iexact=lc_name,
                current=True
            ).exists():
                raise ValidationError(
                    'A product with this name already exists.'
                )

        super().clean()

    def __str__(self):
        return self.product_name

    class Meta:
        ordering = ['date_created']


class ListItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_of_list_item"
    )
    date_created = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="user_who_created_list_item"
    )
    preferred_shop = models.ForeignKey(
        Shop, on_delete=models.SET_NULL, null=True, blank=True
    )
    bought = models.BooleanField(default=False)
    date_bought = models.DateTimeField(default=None, blank=True, null=True)
    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_who_bought_item",
        null=True,
        blank=True
    )
    cancelled = models.BooleanField(default=False)
    date_cancelled = models.DateTimeField(default=None, blank=True, null=True)
    cancelled_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_who_cancelled_item",
        null=True,
        blank=True
    )
    quantity_required = models.IntegerField(default=1)
    quantity_bought = models.IntegerField(default=0)
    shop_bought = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name="shop_where_item_bought",
        null=True,
        blank=True
    )
    creator_notes = models.TextField(null=True, blank=True)
    shopper_notes = models.TextField(null=True, blank=True)
    slug = models.SlugField(null=True, blank=True, unique=True)
    current = models.BooleanField(default=True)

    class Meta:
        ordering = ['date_created']
        verbose_name = "list item"

    def __str__(self):
        return f"{self.product.product_name} \u2013 {self.product.category}"

    def save(self, *args, **kwargs):
        if not self.preferred_shop and self.product.default_shop:
            self.preferred_shop = self.product.default_shop
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(f"{self.product.slug}-{self.id}")
            super().save(update_fields=['slug'])
