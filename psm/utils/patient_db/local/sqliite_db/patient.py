from datetime import date, datetime
from sqlite3 import Error


class Patient:
    """
    Class used to interact with the patient table in SQLite DB.

    Attributes
    ----------
    conn
        the connection to the SQLite DB.
    """

    def __init__(self, conn):
        self.conn = conn

    def search_patient(self, sns_number):
        """
        Search for a patient in the database given its sns number.

        Parameters
        ----------
        sns_number: str
            the patient's sns number

        Returns
        -------
        patient_data: dict
            the patient data
        """

        query = """
            SELECT sns_number, name, gender, phone_number, birth_date, postal_code, locality, address, country, nationality, subsystem
            FROM patient
            WHERE sns_number=?
        """

        cursor = self.conn.cursor()
        res = cursor.execute(query, (sns_number,))

        data = res.fetchone()

        if data is None:
            return None
        

        return {
            'sns_number': data[0],
            'name': data[1],
            'gender': data[2],
            'phone_number': data[3],
            'birth_date': datetime.strptime(data[4], "%Y-%m-%d").strftime("%d/%m/%Y"),
            'postal_code': data[5],
            'locality': data[6],
            'address': data[7],
            'country': data[8],
            'nationality': data[9],
            'subsystem': data[10],
        }

    def add_patient(self, patient_data):
        """
        Method used to add a patient to the database.

        Parameters
        ----------
        patient_data: tuple
            tuple containing all the date necessary to insert a patient in the db.

        Returns
        -------
        created: bool
            indicates if the patient was created with success.
        """

        query = """
            INSERT INTO patient(sns_number, name, gender, phone_number, birth_date, address, postal_code, locality, country, nationality, subsystem)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        try:
            cur = self.conn.cursor()
            cur.execute(query, patient_data)
            self.conn.commit()
        except Error as e:
            print(e)
            return False

        return True
