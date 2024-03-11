import openpyxl
from django.contrib.auth import get_user_model
from django.http import HttpResponse

User = get_user_model()


def download_emails(request):
    wb = openpyxl.Workbook()
    ws = wb.active

    users = User.objects.all()
    ws.append(['Email'])

    for user in users:
        ws.append([user.email])
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=emails.xlsx'

    wb.save(response)

    return response
