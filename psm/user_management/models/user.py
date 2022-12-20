from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from entities.models import CareHouse
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, first_name, last_name):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        if not password:
            raise ValueError('Users must have a password')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password,
            first_name,
            last_name
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    objects = CustomUserManager()

    # The possible user types.
    user_type_choices = [
        ("doctor", "Institution Psychiatrist"),
        ("reviewer", "Referral Reviewer"),
        ("care_house_staff", "Care House Staff"),
        ("financial", "Financial Staff"),
        ("superuser", "Superuser"),
    ]

    username = None

    # Make the email field unique.
    email = models.EmailField(unique=True)

    # The type of this user.
    user_type = models.CharField(max_length=16, choices=user_type_choices)
    # The professional certificate for a psychiatrist.
    professional_certificate = models.CharField(max_length=50, null=True, blank=True)
    # The Care House for a care house user.
    care_house = models.ForeignKey(CareHouse, null=True, blank=True, on_delete=models.SET_NULL)

    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
    ]

    USERNAME_FIELD = 'email'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def clean(self):
        if self.user_type == 'doctor' and self.professional_certificate is None:
            raise ValidationError(
                {
                    'professional_certificate': _(
                        'A professional certificate must be added for a user of type "Institution Psychiatrist"'
                    )
                }
            )

        if self.user_type == 'care_house_staff' and self.care_house is None:
            raise ValidationError(
                {
                    'care_house': _(
                        'A care house must be added for a user of type "Care House Staff"'
                    )
                }
            )
