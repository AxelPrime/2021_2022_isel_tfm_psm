from hashlib import sha256

from asgiref.sync import sync_to_async
from django.db import transaction
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import *

from internment_management.models import InternmentStatus
from internment_management.models import Referral, CareHouseInternment
from internment_management.serializers.referral import EvaluateReferralSerializer
from user_management.models import CustomUser
from utils.api_responses.responses import error_response, success_response
from utils.notifications.notifications import NotificationsManager

ALLOWED_USERS = [
    'care_house_staff',
    'reviewer',
    'superuser'
]
NOTIFICATIONS_TO_CREATE = {
    "awaits_reviewer": {
        "notification_for": ["reviewer"],
        "notification_hide_for": ["care_house_staff", "doctor"],
        "notification_template": "REFERRAL_OPENING_AVAILABLE",
        "notification_read_type": ["referral_creation"],
        "notification_create_type": "referral_opening_indication",
        "readable": False,
        "link": "/reviewer/active-referrals/"
    },
    "referral_rejected": {
        "notification_for": ["reviewer", "care_house_staff",],
        "notification_hide_for": ["doctor", "reviewer", "care_house_staff"],
        "notification_template": "REFERRAL_REJECTED",
        "notification_read_type": ["referral_creation", "referral_opening_indication"],
        "notification_create_type": "referral_evaluation",
        "readable": True,
        "link": "/referrals/history/"
    },
    "referral_approved": {
        "notification_for": ["care_house_staff"],
        "notification_hide_for": ["reviewer"],
        "notification_template": "REFERRAL_APPROVED",
        "notification_read_type": ["referral_opening_indication"],
        "notification_create_type": "referral_evaluation",
        "readable": False,
        "link": "/care-house/pending-internments/"
    }
}
USER_MAPPING = {
    "doctor": "doctor/",
    "care_house_staff": "care-house/",
    "reviewer": "reviewer/",
}


@sync_to_async
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def evaluate_referral_api(request):
    # Obtain the authenticated user.
    user = request.user  # type: CustomUser

    # Verify if the user has the correct user type.
    if user.user_type not in ALLOWED_USERS:
        return error_response(
            HTTP_401_UNAUTHORIZED,
            'Utilizador sem permissões de acesso'
        )
    # Serialize the request body.
    serialized_request = EvaluateReferralSerializer(data=request.data)
    # Validate if the request body is valid.
    if not serialized_request.is_valid():
        return error_response(
            HTTP_400_BAD_REQUEST,
            'Todos os campos devem ser preenchidos',
            data=serialized_request.errors
        )
    # Obtain a dictionary with the valid request data.
    valid_data = serialized_request.validated_data
    # Initiate a transaction.
    with transaction.atomic():
        # Obtain the referrals to change status.
        referrals = Referral.objects.filter(identifier__in=valid_data['referrals'])

        # Obtain the status to change to.
        try:
            status = InternmentStatus.objects.get(label=valid_data['status'])
        except InternmentStatus.DoesNotExist:
            return error_response(
                HTTP_404_NOT_FOUND,
                'Estado não existente'
            )
        # Verify if the next status if valid.
        for ref in referrals:
            if status.label not in ref.current_status.next_states:
                return error_response(
                    HTTP_400_BAD_REQUEST,
                    'Próximo estado inválido'
                )

            notification_manager = None
            notification_data = NOTIFICATIONS_TO_CREATE.get(status.label)
            if notification_data is not None:
                notification_manager = NotificationsManager(
                    notification_data['notification_read_type'],
                    notification_data['notification_create_type']
                )
            if status.label == 'referral_approved':
                time_now = timezone.now()
                internment = CareHouseInternment(
                    identifier=sha256(
                        f"{ref.patient.sns_number}{time_now.date().strftime('%Y-%m-%d')}".encode()
                    ).hexdigest(),
                    referral=ref,
                    admission_date=time_now,
                    admitted_by=user,
                    current_status=InternmentStatus.objects.get(label='awaits_admission')
                )
                internment.save()
                ref.approval_date = time_now
                ref.save()

            if notification_manager is not None:
                for user_type in notification_data['notification_for']:
                    notification_manager.create_notification(
                        notification_for=user_type,
                        template=notification_data['notification_template'],
                        readable=notification_data['readable'],
                        redirect_to=notification_data['link'],
                        referral=ref,
                        invoice=None,
                        care_house=ref.care_house,
                    )

                for user_type in notification_data["notification_hide_for"]:
                    notification_manager.hide_notification(
                        user_type,
                        ref
                    )
        # Update the referrals.
        referrals.update(current_status=status, rejection_reason=valid_data.get('rejection_reason'))

    return success_response(
        False,
        'Estado alterado.'
    )
