from entities.models import CareHouse, MedicalInstitution

CARE_HOUSE_DATA = [
    {
        "code": '1',
        "name": 'Casa de Saúde do Telhal',
        "address": 'Rua A',
    },
    {
        "code": '2',
        "name": 'Casa de Saúde da Idanha',
        "address": 'Rua B',
    },
]

INSTITUTION = [
    {
        "code": "1",
        "name": "Hospital Fernando Fonseca",
        "address": "Rua X",
        "nif": "123456789"
    },
    {
        "code": "2",
        "name": "Hospital Santa Maria",
        "address": "Rua Y",
        "nif": "123456780"
    },
]


def create_care_house():
    for c in CARE_HOUSE_DATA:
        care_house = CareHouse(
            identification_code=c["code"],
            name=c["name"],
            address=c["address"]
        )
        care_house.save()


def create_institutions():
    for i in INSTITUTION:
        institution = MedicalInstitution(
            institution_code=i["code"],
            name=i["name"],
            address=i["address"],
            nif=i["nif"],
        )
        institution.save()
