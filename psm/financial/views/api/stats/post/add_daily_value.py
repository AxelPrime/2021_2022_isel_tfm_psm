from datetime import timedelta

from asgiref.sync import sync_to_async
from django.db import transaction
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import *

from financial.models import DailyValue
from financial.serializers.stats import DailyValueSerializer
from user_management.models import CustomUser
from utils.api_responses.responses import error_response, success_response

ALLOWED_USERS = [
    'superuser'
]


@sync_to_async()
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_daily_value_api(request):
    # Obtain the request user.
    user = request.user  # type: CustomUser
    # Verify if the user can access this API.
    if user.user_type not in ALLOWED_USERS:
        return error_response(
            HTTP_401_UNAUTHORIZED,
            'Utilizador sem permissão de acesso'
        )

    # Serialize the request data.
    serialized_request = DailyValueSerializer(data=request.data)
    # Validate the request data.
    if not serialized_request.is_valid():
        return error_response(
            HTTP_400_BAD_REQUEST,
            'Pedido inválido',
            data=serialized_request.errors
        )
    # Obtain the validated data.
    valid_data = serialized_request.validated_data

    # Begin a transaction.
    with transaction.atomic():
        # Update the previous value.
        prev_value = DailyValue.objects.all().order_by('-id').first()

        # Verify if the new valu can be added.
        if prev_value.start_date >= valid_data['start_date']:
            return error_response(
                HTTP_409_CONFLICT,
                'Não é possível adicionar um novo Valor Diário'
            )
        # Update the previous value's end date.
        if prev_value:
            prev_value.end_date = valid_data['start_date'] - timedelta(days=1)
            prev_value.save()

        # Create the new value.
        daily_value = DailyValue(
            value=valid_data['value'],
            start_date=valid_data['start_date']
        )
        daily_value.save()

    return success_response(
        False,
        'Valore Diário adicionado com sucesso',
    )
