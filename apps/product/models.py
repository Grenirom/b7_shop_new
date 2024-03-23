from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models

from apps.categories.models import Category


class Product(models.Model):
    STATUS_CHOICES = (
        ('in_stock', 'В наличии!'),
        ('out_of_stock', 'Нет в наличии!')
    )

    title = models.CharField(max_length=200, verbose_name='Имя товара')
    article = models.CharField(max_length=20, validators=[
        RegexValidator(r'^[0-9!@#$%^&*()-_+=?]+$'),
    ],
                               verbose_name='Артикул')
    optional_size = models.CharField(max_length=20, blank=True, null=True, verbose_name='Размер товара (опционально)')
    price = models.PositiveIntegerField(verbose_name='Цена')
    quantity = models.IntegerField(default=0, verbose_name='Количество товара')
    description = models.TextField(verbose_name='Описание товара')
    tech_characteristics = models.TextField(blank=True, null=True, verbose_name='Тех. характеристики (опционально)')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория')
    dop_info = models.TextField(blank=True, null=True, verbose_name='Доп. информация (опционально)')
    stock = models.CharField(choices=STATUS_CHOICES, max_length=20, blank=True, null=True, verbose_name='Наличие')
    discount = models.IntegerField(verbose_name='Скидка', blank=True, null=True)

    product = models.ForeignKey('self', on_delete=models.SET_NULL,
                                blank=True, null=True, related_name='various_products')

    def __str__(self):
        return f'{self.title} -> {self.quantity}'

    def save(self, *args, **kwargs):
        if self.quantity > 0:
            self.stock = 'in_stock'
        else:
            self.stock = 'out_of_stock'
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.FileField(upload_to='product-images/')

    def __str__(self):
        return f'Фото товара'

    class Meta:
        verbose_name = 'Фотография товара'
        verbose_name_plural = 'Фотографии товаров'


class ProductHome(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='home-images/')
    url = models.URLField()

    def __str__(self):
        return f'Объявление'

    class Meta:
        verbose_name = 'Объявление на главной странице'
        verbose_name_plural = 'Объявления на главной странице'