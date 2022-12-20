from asgiref.sync import sync_to_async
from django.db.models import Q
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import *

from internment_management.models import CareHouseInternment
from internment_management.serializers.datatables import DataTableRequestSerializer
from user_management.models import CustomUser
from utils.api_responses.responses import error_response

ALLOWED_USER_TYPES = [
    'care_house_staff',
    'superuser',
]

COLUMNS = {
    '1': 'referral__patient__name',
    '2': 'referral__patient__sns_number',
    '3': 'referral__patient__social_security_number',
    '4': 'referral__origin_institution__name',
    '5': 'referral__typology',
}

ORDER = {
    'asc': '',
    'desc': '-'
}


@sync_to_async
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def patients_await_entrance_api(request):
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
    # Serialize the request data.
    serialized_request = DataTableRequestSerializer(data=data)
    # Verify the request data.
    if not serialized_request.is_valid():
        return error_response(
            HTTP_400_BAD_REQUEST,
            'Campos em falta',
            data=serialized_request.errors
        )
    # Obtain the valid data.
    valid_data = serialized_request.validated_data

    # Define the query.
    referral_state = 'awaits_admission'
    query = CareHouseInternment.objects.filter(
        current_status__label=referral_state,
    )

    if user.user_type == 'care_house_staff':
        query = query.filter(referral__care_house=user.care_house)

    # Filter the data with search.
    if valid_data['search']:
        query = query.filter(
            Q(referral__patient__name__icontains=valid_data['search']) |
            Q(referral__patient__sns_number__icontains=valid_data['search']) |
            Q(referral__patient__social_security_number__icontains=valid_data['search']) |
            Q(referral__origin_institution__name__icontains=valid_data['search']) |
            Q(referral__typology__icontains=valid_data['search'])
        )

    # Obtain the data.
    internments_data = [
        [
            f'<input class="form-check-input" type="checkbox" value="" data-referral-id="{i.identifier}">',
            i.referral.patient.name,
            i.referral.patient.sns_number,
            i.referral.patient.social_security_number,
            i.referral.origin_institution.name,
            i.referral.typology,
            f'<a href="javascript:void(0);" data-referral-id="{i.referral.identifier}" onclick="Referrals.getReferralDetails(this)">Ver Detalhes</a>'
        ]
        for i in query.order_by(
            f"{ORDER[valid_data['order_direction']]}{COLUMNS[valid_data['order_column']]}"
        )[valid_data['start']: valid_data['start'] + valid_data['length']]
    ]

    # Define the dataTable data to return.
    datatable_data = {
        'draw': valid_data['draw'],
        'recordsTotal': query.count(),
        'recordsFiltered': len(internments_data),
        'data': internments_data
    }

    return Response(datatable_data)
