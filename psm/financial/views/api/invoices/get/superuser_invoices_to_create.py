from asgiref.sync import sync_to_async
from django.db import transaction
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import *

from entities.models import CareHouse
from financial.utils.check_can_create_invoice import check_can_create_invoice
from utils.api_responses.responses import error_response, success_response

ALLOWED_USERS = [
    'superuser'
]

TYPOLOGIES = [
    'I', 'II', 'III'
]


@sync_to_async()
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def superuser_invoices_to_create_api(request):
    user = request.user  # type: CustomUser

    # Check if the user has access permission.
    if user.user_type not in ALLOWED_USERS:
        return error_response(
            HTTP_401_UNAUTHORIZED,
            'Utilizador sem permissão de acesso',
        )

    # Obtain the care house code.
    care_house_code = request.GET.get('care_house')
    if not care_house_code:
        return error_response(
            HTTP_400_BAD_REQUEST,
            'É necessário indicar a casa de saúde.'
        )

    with transaction.atomic():
        # Obtain the care house.
        try:
            care_house = CareHouse.objects.get(identification_code=care_house_code)
        except CareHouse.DoesNotExist:
            return error_response(
                HTTP_404_NOT_FOUND,
                'Casa de Saúde não encontrada'
            )

        # Obtain the next invoices.
        next_invoices, cookies = check_can_create_invoice(TYPOLOGIES, care_house)

    # Define the response.
    resp = success_response(
        False,
        'Dados obtidos com sucesso',
        data={
            "next_invoices": next_invoices
        }
    )
    # Set the response cookies.
    for c in cookies:
        resp.set_cookie(c['key'], c['value'])

    # Send the response to the client.
    return resp
