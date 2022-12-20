def invoice_files_path(instance, filename):
    """
    Defines the path for upload of the referral files.

    Parameters
    ----------
    instance: Referral
        the instance that is being saved.
    filename: str
        the name of the file
    """
    return f"invoices/{instance.invoice_number}/{filename}"
