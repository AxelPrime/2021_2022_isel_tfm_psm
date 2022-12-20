from ..patient_inerface import PatientInterface
from zeep import Client
from requests.auth import HTTPBasicAuth
from requests import Session
from zeep.transports import Transport


class ServerPatientDb(PatientInterface):

    def __init__(self):
        session = Session()
        session.auth = HTTPBasicAuth("PSM", "M3nTAL#22psm")
        transport = Transport(session=session)

        wsdl = "http://172.16.37.29/hosixfor/Hsoa/hos/patient.asmx?WSDL"

        # service_link = "http://172.16.37.29/hosixfor/Hsoa/hos/patient.asmx"

        self.client = Client(wsdl, transport=transport)

    def search_patient(self, sns_number):
        search_data = {
            "SnsNumber": sns_number
        }

        try:
            response = self.client.service.SearchPatients(search_data)
        except Exception as e:
            print(e)
            response = None

        if response is None:
            return None

        data = response[0]

        return {
            'sns_number': data["SnsNumber"],
            'name': data["PatientName"],
            'gender': data["Sex"],
            'phone_number': data["PhoneNumbers"]["string"][0] if data['PhoneNumbers'] else None,
            'birth_date': data["BirthDate"].strftime("%d/%m/%Y"),
            'postal_code': data["PostalCode"],
            'locality': data["Location"],
            'address': data["Address"],
            'country': data["Country"],
            'nationality': data["Nationality"],
            'subsystem': data["SubsystemCode"],
        }

    def add_patient(self, sns_number, name, gender, phone_number, birth_date, address, postal_code, locality, country,
                    nationality, subsystem):
        req_data = {
            "patient": {
                "InternalNumber": -1000,
                "SnsNumber": sns_number,
                "PatientName": name,
                "BirthDate": birth_date,
                "Sex": gender,
                "Address": address,
                "PostalCode": postal_code,
                "Location": locality,
                "Country": country,
                "Nationality": nationality,
                "FatherName": "",
                "MotherName": "",
                "Exemption": "",
                "ExemptionDesc": "",
                "MaritalState": "",
                "SubsystemCode": subsystem,
                "SubsystemDesc": "",
                "BeneficiaryNumber": "",
                "Profession": -1,
                "DocumentationType": "",
                "Documentation": "",
                "PhoneNumbers": [
                    phone_number
                ],
                "Email": ""
            },
            "userName": "PSM"
        }

        try:
            self.client.service.CreatePatient(**req_data)
        except Exception as e:
            print(e)
            return False

        return True
