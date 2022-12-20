from asgiref.sync import sync_to_async
from django.core.files.temp import NamedTemporaryFile
from django.db import transaction
from django.http import FileResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import *

from financial.models import TypologyStats
from utils.api_responses.responses import error_response
from utils.xlsx_downloads.stats import StatsDownload

ALLOWED_USER_TYPES = [
    "financial",
    "superuser",
]


@sync_to_async()
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def download_care_house_stats_api(request):
    user = request.user  # type: CustomUser

    # Verify if the user has access permissions.
    if user.user_type not in ALLOWED_USER_TYPES:
        return error_response(
            HTTP_401_UNAUTHORIZED,
            "Utilizador sem permissões de acesso."
        )

    # Obtain the year of the data.
    year = request.GET.get('year')
    if not year:
        return error_response(
            HTTP_400_BAD_REQUEST,
            "Pedido inválido"
        )

    # Begin a transaction.
    with transaction.atomic():
        # Obtain the stats.
        try:
            stats = TypologyStats.objects.get(year=year)
        except TypologyStats.DoesNotExist:
            return error_response(
                HTTP_404_NOT_FOUND,
                "Estatísticas não encontradas."
            )

        # Instantiate the stats download class.
        stats_download = StatsDownload(stats)
        # Create the file to download.
        file, filename = stats_download.create_care_house_stats_file()  # type: NamedTemporaryFile, str

        # Create the response.
        response = FileResponse(
            open(file.name, "rb"),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename

        return response
