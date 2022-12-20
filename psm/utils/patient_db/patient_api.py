from ..patient_db.local.local_patient_db import LocalPatientDb
from ..patient_db.server.server_patient_db import ServerPatientDb
from django.conf import settings


def get_patient_interface():
    if settings.PATIENT_DB_TESTING:
        return LocalPatientDb()
    return ServerPatientDb()
