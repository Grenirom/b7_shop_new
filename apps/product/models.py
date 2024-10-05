from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models

from apps.categories.models import Category


class MainPage(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название категории для главной страницы')

    class Meta:
        verbose_name = 'Категория для главной страницы'
        verbose_name_plural = 'Категории для главной страницы'

    def __str__(self):
        return f'{self.title}'


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
    description = models.TextField(blank=True, null=True, verbose_name='Описание товара')
    tech_characteristics = models.TextField(blank=True, null=True, verbose_name='Тех. характеристики (опционально)')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория')
    dop_info = models.TextField(blank=True, null=True, verbose_name='Доп. информация (опционально)')
    stock = models.CharField(choices=STATUS_CHOICES, max_length=20, blank=True, null=True, verbose_name='Наличие')
    discount = models.IntegerField(verbose_name='Скидка', blank=True, null=True)

    product = models.ForeignKey('self', on_delete=models.SET_NULL,
                                blank=True, null=True, related_name='various_products',
                                verbose_name='Родительский товар (для создания одного товара с разными '
                                             'размерами/артикулами/скидками и тд.)')
    main_page_category = models.ForeignKey(MainPage, on_delete=models.SET_NULL,
                                           null=True, blank=True,verbose_name='Категория для товара на главной старнице')

    def __str__(self):
        return f'{self.title} -> {self.quantity} -> {self.optional_size}' if self.optional_size else f'{self.title} -> {self.quantity}'

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


class ProductTechImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='tech_images')
    image = models.FileField(upload_to='product-images/')

    def __str__(self):
        return f'Доп. фото товара для характеристик'

    class Meta:
        verbose_name = 'Фотография для характеристики товара'
        verbose_name_plural = 'Фотографии для характеристик товаров'


class ProductTechCharacteristics(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='tech_char')
    tech_char = models.CharField(max_length=100)

    def __str__(self):
        return f'Доп. характеристики для товара'

    class Meta:
        verbose_name = 'Доп. характеристики для товара'
        verbose_name_plural = 'Доп. характеристики для товаров'


class ProductHome(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    description = models.CharField(max_length=200, verbose_name='Описание')
    image = models.ImageField(upload_to='home-images/', verbose_name='Картинка')
    url = models.URLField()

    def __str__(self):
        return f'Объявление'

    class Meta:
        verbose_name = 'Объявление на главной странице'
        verbose_name_plural = 'Объявления на главной странице'
