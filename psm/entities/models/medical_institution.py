from django.db import models


class MedicalInstitution(models.Model):
    # The identification code of this institution.
    institution_code = models.CharField(max_length=25, unique=True)
    # The name of the institution.
    name = models.CharField(max_length=128)
    # The address of the institution.
    address = models.CharField(max_length=256)
    # The NIF of the institution.
    nif = models.CharField(max_length=9, unique=True)

    def __str__(self):
        return self.name
