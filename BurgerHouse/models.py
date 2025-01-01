from django.db import models
from datetime import datetime

# Foydalanuvchi modeli
class Foydalanuvchi(models.Model):
    telegram_id = models.BigIntegerField(
        unique=True,
        verbose_name="Telegram ID"
    )
    full_name = models.CharField(
        max_length=255,
        verbose_name="To'liq ism"
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        verbose_name="Foydalanuvchi nomi"
    )
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name="Telefon raqami"
    )

    def __str__(self):
        return self.username if self.username else self.full_name

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"


# Category modeli
class Category(models.Model):
    name_uz = models.CharField(
        max_length=120,
        verbose_name="Kategoriya nomi (UZ)"
    )
    name_ru = models.CharField(
        max_length=120,
        verbose_name="Kategoriya nomi (RU)"
    )
    image = models.ImageField(
        upload_to="images/",
        blank=True,
        null=True,
        verbose_name="Rasm"
    )

    def __str__(self):
        return self.name_uz

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"


# Product modeli
class Product(models.Model):
    STATUS_PRODUCT = [
        ('Yes', 'Bor'),
        ('No', 'Hozircha yo`q'),
    ]

    product_name_uz = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Mahsulot nomi (UZ)"
    )
    product_name_ru = models.CharField(
        max_length=255,
        verbose_name="Mahsulot nomi (RU)"
    )
    product_image = models.ImageField(
        upload_to="images/",
        verbose_name="Mahsulot rasmi"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Kategoriya"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Narx"
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_PRODUCT,
        default='Yes',
        verbose_name="Holat"
    )
    discount = models.PositiveIntegerField(
        default=0,
        verbose_name="Mahsulot chegirmadagi narxi"
    )

    def __str__(self):
        return self.product_name_uz

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"


# Order modeli
class Order(models.Model):
    STATUS_CHOICES = [
        ('Waiting', 'Kutilmoqda'),
        ('received', 'Qabul qilindi'),
        ('preparing', 'Tayyorlanmoqda'),
        ('delivering', 'Yetkazilmoqda'),
        ('delivered', 'Yetkazib berildi'),
        ('new', 'Yangi'),  # Yangi holat qo'shildi
    ]

    owner = models.ForeignKey(
        Foydalanuvchi,
        on_delete=models.CASCADE,
        verbose_name="Buyurtmachi",
        related_name='orders'
    )
    products = models.ManyToManyField(
        Product,
        through='OrderProduct',
        verbose_name="Mahsulotlar"
    )
    address = models.TextField(
        verbose_name="Buyurtma manzili"
    )
    additional_phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name="Qo'shimcha telefon"
    )

    note = models.TextField(
        blank=True,
        null=True,
        verbose_name="Eslatma"
    )

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name="Kenglik"
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name="Uzunlik"
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='new',  # Default holat 'Yangi' bo'lishi kerak
        verbose_name="Buyurtma holati"
    )

    def __str__(self):
        return f"Order #{self.id} by {self.owner.username}"

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"


# Order va Product o'rtasidagi bog'lovchi model
class OrderProduct(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name="Buyurtma",
        related_name="order_products"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Mahsulot"
    )
    order_count = models.PositiveIntegerField(
        default=1,
        verbose_name="Mahsulot soni"
    )

    def __str__(self):
        return f"Product {self.product.product_name_uz} in Order #{self.order.id}"

    class Meta:
        verbose_name = "Buyurtma mahsuloti"
        verbose_name_plural = "Buyurtma mahsulotlari"

