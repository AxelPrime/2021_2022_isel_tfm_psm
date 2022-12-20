from base64 import urlsafe_b64encode
from datetime import date
from hashlib import md5
from datetime import datetime

from cryptography.fernet import Fernet

KEY = urlsafe_b64encode(md5(b"wXvNtqGgUgbXCjWu2sbs").hexdigest().encode())


class DateEncryption:
    date_format = '%Y-%m-%d'

    def __init__(self):
        self.fernet = Fernet(KEY)

    def encrypt(self, start_date: date, end_date: date):
        """
        Encrypt the 2 given dates as a single string.

        Parameters:
            start_date (date): the first date
            end_date (date): the final date

        Returns:
            encrypted (str): The encrypted string.
        """
        message = f"{start_date.strftime(self.date_format)}|{end_date.strftime(self.date_format)}"

        return self.fernet.encrypt(message.encode()).decode()

    def decrypt(self, encrypted: str):
        """
        Decrypt a given string into 2 dates.

        Parameters
        ----------
        encrypted: str
            the string to decrypt

        Returns
        -------
        dates: tuple
            the 2 string decrypted
        """
        decrypted = self.fernet.decrypt(encrypted.encode()).decode()

        dates_split = decrypted.split('|')

        start_date = datetime.strptime(dates_split[0], self.date_format).date()
        end_date = datetime.strptime(dates_split[1], self.date_format).date()

        return start_date, end_date
