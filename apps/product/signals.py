from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.product.models import ProductDiscount
from apps.product.serializers import ProductListSerializer


@receiver([post_save, post_delete], sender=ProductDiscount)
def update_discounted_price(sender, instance, **kwargs):
    affected_products = instance.product.all()
    print('SIGNAL WORKED _------------------')
    for product in affected_products:
        product_serializer = ProductListSerializer(product)
        updated_discounted_price = product_serializer.get_discounted_price(product)
        product_serializer.data['discounted_price'] = updated_discounted_price


def calculate_discounted_price(product):
    try:
        product_discount = ProductDiscount.objects.get(product=product)
        discounted_price = product.price - (product.price * product_discount.discount / 100)
        return discounted_price
    except ProductDiscount.DoesNotExist:
        return None