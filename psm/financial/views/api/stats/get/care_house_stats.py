from django.db import transaction
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import *

from financial.serializers.stats import StatsSerializer
from user_management.models import CustomUser
from utils.api_responses.responses import error_response, success_response
from asgiref.sync import sync_to_async
from financial.models import TypologyStats

ALLOWED_USER_TYPES = [
    'financial',
    'superuser',
]

MONTHS = {
    '1': 'Janeiro',
    '2': 'Fevereiro',
    '3': 'Março',
    '4': 'Abril',
    '5': 'Maio',
    '6': 'Junho',
    '7': 'Julho',
    '8': 'Agosto',
    '9': 'Setembro',
    '10': 'Outubro',
    '11': 'Novembro',
    '12': 'Dezembro',
}


@sync_to_async()
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def care_house_stats_api(request):
    # Obtain the authenticated user.
    user = request.user  # type: CustomUser
    # Check if the user has access permissions.
    if user.user_type not in ALLOWED_USER_TYPES:
        return error_response(
            HTTP_401_UNAUTHORIZED,
            'Utilizador sem permissão de acesso'
        )

    # Serialize the request.
    serialized_request = StatsSerializer(data=request.GET)
    # Validate the data.
    if not serialized_request.is_valid():
        return error_response(
            HTTP_400_BAD_REQUEST,
            'Pedido inválido'
        )
    valid_data = serialized_request.validated_data

    # Begin transaction.
    with transaction.atomic():
        # Obtain the stats for the given year.
        try:
            stats = TypologyStats.objects.get(year=valid_data['year'])
        except TypologyStats.DoesNotExist:
            return error_response(
                HTTP_404_NOT_FOUND,
                'Dados não encontrados'
            )

        # Obtain the data.
        stats_data = [
            [
                MONTHS[month_number],
                data['total_patients'],
                data['total_dailies'],
                data['total_amount']
            ]
            for month_number, data in sorted(
                stats.care_house_stats[valid_data['typology']][valid_data['care_house']]['months'].items(),
                key=lambda t: int(t[0])
            )
        ]

    # Return the data.
    return success_response(
        False,
        'Dados obtidos',
        {
            'stats': stats_data,
        }
    )
