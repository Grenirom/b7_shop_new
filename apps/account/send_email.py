from decouple import config
from django.core.mail import send_mail

HOST = config('HOST_FOR_SEND_EMAIL')


def send_confirmation_email(user, code):
    link = f'http://{HOST}/api/account/activate/{code}/'

    send_mail(
        'Здравствуйте, активируйте ваш аккаунт!',
        f'Чтобы активировать ваш аккаунт нужно перейти по ссылке ниже:'
        f'\n{link}'
        f'\nСсылка работает один раз!',
        'ngrebnev17@gmail.com',
        [user],
        fail_silently=False,
    )
