from django.contrib.auth import get_user_model
from django.db import models

from apps.product.models import Product


User = get_user_model()


class OrderItem(models.Model):
    order = models.ForeignKey('Order', related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f'{self.product}'

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='пользователь')
    name = models.CharField(max_length=150, verbose_name='Имя пользователя')
    products = models.ManyToManyField(Product, through=OrderItem, verbose_name='товары')
    phone_number = models.CharField(max_length=13, verbose_name='Номер телефона')
    shipping_address = models.CharField(max_length=250, verbose_name='Адрес доставки')
    total_sum = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Общая сумма')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')

    def __str__(self):
        return f'{self.user} - {self.created_at}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
