from decouple import config
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

OWNER_EMAIL = config('OWNER_EMAIL')
LINK = config('LINK')



def send_order_notification_email(email, order_id, total_sum):
    subject = 'Оповещение о создании заказа'
    html_message = render_to_string('emails/order_notification.html', {'order_id': order_id, 'total_sum': total_sum})
    plain_message = strip_tags(html_message)  # Преобразуем HTML в обычный текст
    from_email = 'ngrebnev17@gmail.com'  # Замените на ваш email
    to_email = email
    # Создаем EmailMultiAlternatives объект для отправки как HTML, так и обычного текста
    email_message = EmailMultiAlternatives(subject, plain_message, from_email, [to_email])
    email_message.attach_alternative(html_message, "text/html")  # Прикрепляем HTML-версию
    email_message.send()


def send_order_email_to_owner(order_id, total_sum, created_at, shipping_address):

    formatted_created_at = created_at.strftime("%d-%m-%Y")

    html_message = render_to_string(
        'emails/order_notification_to_owner.html',
        {
            'order_id': order_id,
            'total_sum': total_sum,
            'shipping_address': shipping_address,
            'admin_panel_link': 'https://backend.b7.kg/admin/orders/order/',  # Замените на вашу ссылку
        }
    )

    send_mail(
        'Оповещение о создании нового заказа',
        '',
        'ngrebnev17@gmail.com',
        [OWNER_EMAIL],
        fail_silently=False,
        html_message=html_message
    )