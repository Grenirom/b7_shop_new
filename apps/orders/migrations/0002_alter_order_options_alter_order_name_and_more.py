# Generated by Django 5.0.1 on 2024-01-31 08:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
        ('product', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.AlterField(
            model_name='order',
            name='name',
            field=models.CharField(max_length=150, verbose_name='Имя пользователя'),
        ),
        migrations.AlterField(
            model_name='order',
            name='phone_number',
            field=models.CharField(max_length=13, verbose_name='Номер телефона'),
        ),
        migrations.AlterField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(through='orders.OrderItem', to='product.product', verbose_name='товары'),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_address',
            field=models.CharField(max_length=250, verbose_name='Адрес доставки'),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_sum',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Общая сумма'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
    ]
