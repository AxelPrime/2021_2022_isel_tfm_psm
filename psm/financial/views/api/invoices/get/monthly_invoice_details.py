from django.db import transaction
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import *
from asgiref.sync import sync_to_async
from financial.models import MonthlyInvoice
from user_management.models import CustomUser
from utils.api_responses.responses import error_response, success_response

ALLOWED_USER_TYPES = [
    'care_house_staff',
    'financial',
    'superuser'
]

@sync_to_async()
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def monthly_invoice_details_api(request):
    # Get the authenticated user.
    user = request.user  # type: CustomUser
    # Check if the user has access permission.
    if user.user_type not in ALLOWED_USER_TYPES:
        return error_response(
            HTTP_401_UNAUTHORIZED,
            'Utilizador sem permissão de acesso',
        )

    # Obtain the invoice number.
    invoice_number = request.GET.get('invoice_number')
    # Check if invoice number is filled.
    if not invoice_number:
        return error_response(
            HTTP_400_BAD_REQUEST,
            'Pedido inválido'
        )

    # Begin transaction.
    with transaction.atomic():
        # Obtain the invoice.
        try:
            invoice = MonthlyInvoice.objects.get(invoice_number=invoice_number)
        except MonthlyInvoice.DoesNotExist:
            return error_response(
                HTTP_404_NOT_FOUND,
                'Listagem não encontrada',
            )

        # Map the invoice lines data.
        invoice_lines = [
            [
                i['patient_name'],
                i['invoice_start'],
                i['invoice_end'],
                i['total_days'],
                i['total_amount'],
                f'<a href="javascript:void(0)" data-internment-id="{i["internment_id"]}" data-bs-dismiss="modal" onclick="Internments.getActivityLog(this)">Ver Atividade</a>',
                f'<a href="javascript:void(0)" data-referral-id="{i["referral_id"]}" data-bs-dismiss="modal" onclick="Referrals.getReferralDetails(this)">Ver Detalhes</a>'
            ]
            for i in invoice.invoice_lines['data']
        ]
        # Get the invoice line details.
        response_data = {
            'invoice_lines': invoice_lines,
            'is_final': invoice.status != 'temp',
            'month': invoice.get_month_display(),
            'year': invoice.year
        }

    return success_response(
        False,
        'Dados obtidos com sucesso',
        data=response_data
    )

