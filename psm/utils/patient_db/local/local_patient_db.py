from ..patient_inerface import PatientInterface
from .sqliite_db.patient import Patient
import sqlite3
from sqlite3 import Error


class LocalPatientDb(PatientInterface):
    """
    Class used to interact with the local Patient Database.
    """
    conn = None
    patient_api = None

    def __init__(self):
        try:
            self.conn = sqlite3.connect('sqlite.patient.db')
            self.patient_api = Patient(self.conn)
        except Error as e:
            print(e)
            raise e

    def search_patient(self, sns_number):
        """
        Method used to search for a patient.

        Parameters
        ----------
        sns_number: str
            the patient sns number

        Returns
        -------
        patient_data: dict
            a dictionary containing the patient data
        """
        return self.patient_api.search_patient(sns_number)

    def add_patient(self, sns_number, name, gender, phone_number, birth_date, address, postal_code, locality, country, nationality, subsystem):
        """
        Method used to add a patient to the database.

        Parameters
        ----------
        sns_number: str
            the patient's sns number
        name: str
            the patient's full name
        gender: str
            the gender of the patient
        phone_number: str
            the patient's phone_number
        birth_date: date
            the date of birth of the patient
        address: str
            the address of the patient
        postal_code: str
            the patient's postal code
        locality: str
            the patient's locality
        country: str
            the country of the patient
        nationality: str
            the patient's nationality
        subsystem: str
            the patient's insurance subsystem

        Returns
        -------
        created: bool
            indicates if the patient was created with success.
        """
        return self.patient_api.add_patient(
            (sns_number, name, gender, phone_number, birth_date, address, postal_code, locality, country, nationality, subsystem)
        )
