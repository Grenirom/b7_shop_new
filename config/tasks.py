from rest_framework.response import Response

from .celery import app
from apps.orders.send_email import send_order_notification_email, send_order_email_to_owner


@app.task
def send_order_notification_to_user_task(email, order_id, total_sum):
    try:
        send_order_notification_email(email, order_id, total_sum)
    except Exception as e:
        return Response('При отправке сообщения на почту что-то пошло не так')


@app.task
def send_order_email_to_owner_task(order_id, total_sum, created_at, shipping_address):
    try:
        send_order_email_to_owner(order_id, total_sum, created_at, shipping_address)
    except Exception as e:
        return Response('Что-то пошло не так!')
