from django.db import transaction
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import *

from user_management.models import CustomUser
from utils.api_responses.responses import error_response, success_response
from asgiref.sync import sync_to_async
from financial.models import TypologyIIMonthlyStats
from financial.serializers.stats.typology_ii_stats_serializer import TypologyStatsSerializer

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
def typology_ii_stats_api(request):
    # Obtain the authenticated user.
    user = request.user  # type: CustomUser
    # Check if the user has access permissions.
    if user.user_type not in ALLOWED_USER_TYPES:
        return error_response(
            HTTP_401_UNAUTHORIZED,
            'Utilizador sem permissão de acesso'
        )

    # Serialize the request.
    serialized_request = TypologyStatsSerializer(data=request.GET)
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
            stats = TypologyIIMonthlyStats.objects.get(year=valid_data['year'])
        except TypologyIIMonthlyStats.DoesNotExist:
            return error_response(
                HTTP_404_NOT_FOUND,
                'Dados não encontrados'
            )

        # Obtain the data.
        stats_data = [
            [
                data['name'],
                data['nif'],
                code,
                data['data']['total_patients'],
                data['data']['amount']
            ]
            for code, data in stats.data['institutions'].items()
        ]

    # Return the data.
    return success_response(
        False,
        'Dados obtidos',
        {
            'stats': stats_data,
        }
    )
