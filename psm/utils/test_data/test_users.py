from entities.models import CareHouse
from user_management.models import CustomUser

USER_DATA = [
    {
        "email": "doctor@mail.com",
        "first_name": "Mr",
        "last_name": "Doctor",
        "user_type": "doctor",
        "password": "caranguejo2k9",
        "professional_certificate": "1",
        "care_house_id": None
    },
    {
        "email": "reviewer@mail.com",
        "first_name": "Mr",
        "last_name": "Reviewer",
        "user_type": "reviewer",
        "password": "caranguejo2k9",
        "professional_certificate": None,
        "care_house_id": None
    },
    {
        "email": "care_house@mail.com",
        "first_name": "Mr",
        "last_name": "Care House",
        "user_type": "care_house_staff",
        "password": "caranguejo2k9",
        "professional_certificate": None,
        "care_house_id": 1
    },
    {
        "email": "financial@mail.com",
        "first_name": "Mr",
        "last_name": "Financial",
        "user_type": "financial",
        "password": "caranguejo2k9",
        "professional_certificate": None,
        "care_house_id": None
    },
    {
        "email": "superuser@mail.com",
        "first_name": "Mr",
        "last_name": "Superuser",
        "user_type": "superuser",
        "password": "caranguejo2k9",
        "professional_certificate": None,
        "care_house_id": None
    },
]


def create_test_users():
    # Iterate the data.
    for i in USER_DATA:
        try:
            CustomUser.objects.get(email=i["email"])
        except CustomUser.DoesNotExist:
            user = CustomUser.objects.create_user(
                i["email"],
                i["password"],
                i['first_name'],
                i['last_name']
            )
            user.user_type = i["user_type"]
            user.care_house = CareHouse.objects.get(identification_code=i["care_house_id"]) if i["care_house_id"] else None
            user.professional_certificate = i["professional_certificate"]
            user.save()
