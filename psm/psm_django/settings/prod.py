from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Used to indicate if the Patient DB is in testing mode.
PATIENT_DB_TESTING = False

DATABASES = {
    # Local DB
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config("PROD_DB_NAME"),
        'USER': config("PROD_DB_USER"),
        'PASSWORD': config("PROD_DB_PASSWORD"),
        'HOST': 'localhost',
        'PORT': '',
    }
}
