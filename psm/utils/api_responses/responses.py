from rest_framework.response import Response
from rest_framework.status import *


def error_response(status_code: int, message: str, data=None):
    return Response({
        'success': False,
        'message': message,
        'data': data
    }, status=status_code)


def success_response(created: bool, message: str, data=None):
    return Response({
        'success': True,
        'message': message,
        'data': data
    }, status=HTTP_201_CREATED if created else HTTP_200_OK)
