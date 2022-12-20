from asgiref.sync import sync_to_async
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import *

from financial.models import YearlyInvoice
from internment_management.serializers.datatables import DataTableRequestSerializer
from utils.api_responses.responses import error_response

ALLOWED_USER_TYPES = [
    'financial',
    'superuser',
]

COLUMNS = {
    '0': 'referral__patient__name',
    '1': 'referral__patient__sns_number',
    '2': 'referral__patient__social_security_number',
    '3': 'referral__typology',
    '4': 'current_status__name',
}

ORDER = {
    'asc': '',
    'desc': '-'
}


@sync_to_async()
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_yearly_invoice_data_api(request):
    # Obtain the authenticated user.
    user = request.user  # type: CustomUser
    # Verify if the user has permissions to access this data.
    if user.user_type not in ALLOWED_USER_TYPES:
        return error_response(HTTP_401_UNAUTHORIZED, 'You do not have permission to access this content')

    # Define the request data to serialize.
    data = {
        'draw': request.GET.get('draw'),
        'order_column': request.GET.get('order[0][column]'),
        'order_direction': request.GET.get('order[0][dir]'),
        'start': request.GET.get('start'),
        'length': request.GET.get('length'),
        'search': request.GET.get('search[value]'),
    }
    invoice_number = request.GET.get("invoice_number")
    # Serialize the request data.
    serialized_request = DataTableRequestSerializer(data=data)
    # Verify the request data.
    if not serialized_request.is_valid() or not invoice_number:
        return error_response(
            HTTP_400_BAD_REQUEST,
            'Campos em falta',
            data=serialized_request.errors
        )
    # Obtain the valid data.
    valid_data = serialized_request.validated_data

    # Obtain the invoice.
    try:
        yearly_invoice = YearlyInvoice.objects.get(invoice_number=invoice_number)
    except YearlyInvoice.DoesNotExist:
        return error_response(
            HTTP_404_NOT_FOUND,
            'Invoice not found.'
        )

    # Get the invoice data.
    return_data = yearly_invoice.data['lines'][valid_data['start']: valid_data['start'] + valid_data['length']]

    # Define the dataTable data to return.
    datatable_data = {
        'draw': valid_data['draw'],
        'recordsTotal': len(yearly_invoice.data['lines']),
        'recordsFiltered': len(return_data),
        'data': return_data
    }

    return Response(datatable_data)
