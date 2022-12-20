from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Used to indicate if the Patient DB is in testing mode.
PATIENT_DB_TESTING = True

DATABASES = {
    # Local DB
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config("DEV_DB_NAME"),
        'USER': config("DEV_DB_USER"),
        'PASSWORD': config("DEV_DB_PASSWORD"),
        'HOST': 'localhost',
        'PORT': '',
    }
}
