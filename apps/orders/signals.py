from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_save
from rest_framework.response import Response

# from .send_email import send_order_notification_email
from .models import Order, OrderItem
from config.tasks import send_order_notification_to_user_task, send_order_email_to_owner_task
from .send_email import send_order_email_to_owner


@receiver(pre_delete, sender=OrderItem)
def return_products_to_stock(sender, instance, **kwargs):
    product = instance.product
    quantity = instance.quantity
    product.quantity += quantity
    product.save()


@receiver(post_save, sender=Order)
def order_post_save(sender, instance, created, **kwargs):
    if created:
        try:
            send_order_notification_to_user_task.delay(instance.user.email, instance.id,
                                                       instance.total_sum)

            send_order_email_to_owner_task.delay(instance.id, instance.total_sum,
                                        instance.created_at, instance.shipping_address)
            # print(created_at_formatted, 'time----------------------')
        except Exception as e:
            return Response('При отправке сообщения на почту что-то пошло не так')
