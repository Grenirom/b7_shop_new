from decouple import config
from django.core.mail import send_mail


def send_order_notification_email(email, order_id, total_sum):
    send_mail(
        'Оповещение о создании заказа',
        f'Здравствуйте, с вашего аккаунта был создан заказ №{order_id}\n'
        f'Полная сумма заказа составила: {total_sum} сом\n'
        f'Спасибо за доверие\n'
        f'b7.kg',
        'ngrebnev17@gmail.com',
        [email],
        fail_silently=False
    )


OWNER_EMAIL = config('OWNER_EMAIL')
LINK = config('LINK')


def send_order_email_to_owner(order_id, total_sum, created_at, shipping_address):

    formatted_created_at = created_at.strftime("%d-%m-%Y")

    send_mail(
        'Оповещение о создании нового заказа',
        f'Здравствуйте! {formatted_created_at} был создан новый заказ №{order_id}.\n'
        f'Общая сумма заказа составила {total_sum} сом.\n'
        f'Адрес доставки: {shipping_address}\n'
        f'Для более подробной информации, перейдите в Админ Панель:\n'
        f'{LINK}',
        'ngrebnev17@gmail.com',
        [OWNER_EMAIL],
        fail_silently=False
    )