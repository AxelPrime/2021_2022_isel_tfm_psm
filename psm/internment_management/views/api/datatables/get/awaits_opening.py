from django.db.models import Q
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from internment_management.models import Referral
from internment_management.serializers.datatables import DataTableRequestSerializer
from user_management.models import CustomUser
from utils.api_responses.responses import error_response, success_response
from asgiref.sync import sync_to_async
from rest_framework.status import *

ALLOWED_USER_TYPES = [
    'care_house_staff',
    'superuser',
]

COLUMNS = {
    '1': 'patient__name',
    '2': 'patient__sns_number',
    '3': 'patient__social_security_number',
    '4': 'origin_institution__name',
    '5': 'care_house__name',
    '6': 'typology',
    '7': 'current_status__name',
}

ORDER = {
    'asc': '',
    'desc': '-'
}


@sync_to_async
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def awaits_opening_api(request):
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
    referral_state = ['awaits_care_house', 'awaits_opening']
    query = Referral.objects.filter(
        current_status__label__in=referral_state,
    )

    # Check if it's a care house access.
    if user.user_type == 'care_house_staff':
        query = query.filter(care_house=user.care_house)

    # Filter the data with search.
    if valid_data['search']:
        query = query.filter(
            Q(patient__name__icontains=valid_data['search']) |
            Q(patient__sns_number__icontains=valid_data['search']) |
            Q(patient__social_security_number__icontains=valid_data['search']) |
            Q(origin_institution__name__icontains=valid_data['search']) |
            Q(typology__icontains=valid_data['search'])
        )

    # Obtain the data.
    referrals_data = [
        [
            f'<input class="form-check-input" type="checkbox" value="" data-referral-id="{i.identifier}">',
            i.patient.name,
            i.patient.sns_number,
            i.patient.social_security_number,
            i.origin_institution.name,
            i.care_house.name,
            i.typology,
            i.current_status.name,
            f'<a href="javascript:void(0);" data-referral-id="{i.identifier}" onclick="Referrals.getReferralDetails(this)">Ver Detalhes</a>'
        ]
        for i in query.order_by(
            f"{ORDER[valid_data['order_direction']]}{COLUMNS[valid_data['order_column']]}"
        )[valid_data['start']: valid_data['start'] + valid_data['length']]
    ]

    # Define the dataTable data to return.
    datatable_data = {
        'draw': valid_data['draw'],
        'recordsTotal': query.count(),
        'recordsFiltered': len(referrals_data),
        'data': referrals_data
    }

    return Response(datatable_data)
