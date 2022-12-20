from asgiref.sync import sync_to_async
from django.db import transaction
from django.http import FileResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import *

from financial.models import YearlyInvoice
from user_management.models import CustomUser
from utils.api_responses.responses import error_response
from utils.xlsx_downloads import YearlyInvoiceDownload
from django.core.files.temp import NamedTemporaryFile

ALLOWED_USER_TYPES = [
    "financial",
    "superuser",
]


@sync_to_async()
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def download_yearly_invoice_api(request):
    user = request.user  # type: CustomUser

    # Verify if the user has access permissions.
    if user.user_type not in ALLOWED_USER_TYPES:
        return error_response(
            HTTP_401_UNAUTHORIZED,
            "Utilizador sem permissões de acesso."
        )

    # Obtain the invoice invoice_number.
    invoice_number = request.GET.get('invoice_number')
    # Verify if the request is valid.
    if not invoice_number:
        return error_response(
            HTTP_400_BAD_REQUEST,
            "Pedido inválido"
        )

    # Begin transaction.
    with transaction.atomic():
        # Obtain the invoice.
        try:
            invoice = YearlyInvoice.objects.get(invoice_number=invoice_number)
        except YearlyInvoice.DoesNotExist:
            return error_response(
                HTTP_404_NOT_FOUND,
                "Recibo não encontrado"
            )

        # Instantiate the invoice creation class.
        invoice_download = YearlyInvoiceDownload(invoice, NamedTemporaryFile(suffix=".xlsx"))
        # Create the temp file.
        filepath = invoice_download.create_invoice_xlsx()
        response = FileResponse(
            open(invoice_download.temp_file.name, "rb"),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filepath

        return response
