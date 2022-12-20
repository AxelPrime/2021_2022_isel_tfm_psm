from django.db import transaction
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from asgiref.sync import sync_to_async

from internment_management.models import Referral
from user_management.models import CustomUser
from utils.api_responses.responses import error_response, success_response
from django.http.response import HttpResponse, FileResponse
from rest_framework.status import *

ALLOWED_USER_TYPES = [
    'doctor',
    'reviewer',
    'financial',
    'care_house_staff',
    'superuser'
]


@sync_to_async
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def download_responsibility_term_api(request):
    # Obtain the referral ID.
    ref_id = request.GET.get('referral_id')
    if not ref_id:
        return error_response(HTTP_400_BAD_REQUEST, 'Pedido inválido')

    # Verify if the user has access.
    user = request.user  # type: CustomUser
    if user.user_type not in ALLOWED_USER_TYPES:
        return error_response(HTTP_401_UNAUTHORIZED, 'Utilizador sem permissão de acesso')

    # Begin transaction.
    with transaction.atomic():
        try:
            referral = Referral.objects.get(identifier=ref_id)
        except Referral.DoesNotExist:
            return error_response(HTTP_404_NOT_FOUND, 'Referenciação não encontrada')

        if user.user_type == 'care_house_staff' and referral.care_house != user.care_house:
            return error_response(HTTP_401_UNAUTHORIZED, 'Utilizador sem permissão de acesso')

        filename = f'Termo_Responsabilidade_{referral.patient.name}.pdf'
        response = FileResponse(referral.responsibility_term, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response
