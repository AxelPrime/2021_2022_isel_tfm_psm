from asgiref.sync import sync_to_async
from django.db import transaction
from django.http.response import FileResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import *

from financial.models import MonthlyInvoice
from internment_management.models import Referral
from user_management.models import CustomUser
from utils.api_responses.responses import error_response

ALLOWED_USER_TYPES = [
    'care_house_staff',
    'financial',
    'superuser'
]


@sync_to_async
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def download_invoice_file_api(request):
    # Obtain the referral ID.
    invoice_number = request.GET.get('invoice_number')
    if not invoice_number:
        return error_response(HTTP_400_BAD_REQUEST, 'Pedido inválido')

    # Verify if the user has access.
    user = request.user  # type: CustomUser
    if user.user_type not in ALLOWED_USER_TYPES:
        return error_response(HTTP_401_UNAUTHORIZED, 'Utilizador sem permissão de acesso')

    # Begin transaction.
    with transaction.atomic():
        try:
            invoice = MonthlyInvoice.objects.get(invoice_number=invoice_number)
        except Referral.DoesNotExist:
            return error_response(HTTP_404_NOT_FOUND, 'Referenciação não encontrada')

        if user.user_type == 'care_house_staff' and invoice.care_house != user.care_house:
            return error_response(HTTP_401_UNAUTHORIZED, 'Utilizador sem permissão de acesso')

        filename = f'Recibo_{invoice.care_house.name.replace(" ", "_")}_{invoice.get_month_display()}_{invoice.year}.pdf'
        response = FileResponse(invoice.invoice_file, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response
