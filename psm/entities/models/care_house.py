from django.db import models


class CareHouse(models.Model):
    # The identifier of this care house.
    identification_code = models.CharField(max_length=25, unique=True)
    # The name of the care house.
    name = models.CharField(max_length=128)
    # The address of the care house.
    address = models.CharField(max_length=256)

    def __str__(self):
        return self.name
