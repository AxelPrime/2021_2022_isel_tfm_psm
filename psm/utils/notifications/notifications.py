import uuid

from django.db.models import Q

from user_management.models import Notifications, NotificationTemplate


class NotificationsManager:
    """
    Class used to manage the creation and update of notiifications.

    Attributes
    ----------
    read_type: str
        the type of notifications that can be read.

    create_type: list
        the type of notifications that can be created.
    """

    def __init__(self, read_type="", create_type=None):
        self.create_type = create_type
        self.read_type = read_type

    def create_notification(
            self,
            notification_for: str,
            template: str,
            readable: bool,
            redirect_to: str,
            referral=None,
            invoice=None,
            care_house=None
    ):
        """
        Create a new notification.

        Parameters
        ----------
        notification_for: str
            the user type that the notification is for.

        template: str
            the notification template id.

        readable: bool
            indicates if the notification is readable on click.

        redirect_to: str
            the link to which the notification redirects to.

        referral: Referral
            the referral that this notification is supposed to accompany.

        invoice: MonthlyInvoice
            the invoice that this notification is supposed to accompany.

        care_house: CareHouse
            the care house that will see this notification.

        Returns
        -------
        success, error: tuple
            indicates if the creation was a success, and the error if there was one.
        """

        # Check if the type is valid.
        if not self.create_type.startswith(("referral_", "invoice_")):
            return False, "Tipo de notificação inválido"
        # Check if the care house if set.
        if notification_for == "care_house_staff" and care_house is None:
            return False, "É necessário indicar uma Casa de Saúde"
        # Create the notification object.
        notification = Notifications(
            identifier=uuid.uuid4(),
            notification_type=self.create_type,
            process_type=self.create_type.split("_")[0],
            user_type=notification_for,
            care_house=care_house,
            readable_on_click=readable,
            redirect_to=redirect_to,
            template=NotificationTemplate.objects.get(identifier=template),
        )
        # Handle referral ntifications.
        if self.create_type.startswith("referral_"):
            if referral is None:
                return False, "É necessário indicar uma referenciação"
            notification.referral = referral
        # Handle receipt notifications.
        elif self.create_type.startswith("invoice_"):
            if invoice is None:
                return False, "É necessário indicar um recibo"
            notification.receipt = invoice
        # Save the notification.
        notification.save()

        return True, None

    def hide_notification(
            self,
            notification_for: str,
            referral=None,
            invoice=None,
    ):
        """
        Hide a notification.

        Parameters
        ----------
        notification_for: str
            the user thype that the notification is for.

        referral: Referral
            the referral that this notification is supposed to accompany.

        invoice: MonthlyInvoice
            the invoice that this notification is supposed to accompany.

        Returns
        -------
        notification, error: tuple
            indicates if the creation was a success, and the error if there was one.
        """

        query = Q(notification_type__in=self.read_type) & Q(user_type=notification_for) & Q(display=True) & Q(
            referral=referral) & Q(receipt=invoice)

        try:
            notification = Notifications.objects.filter(query)
        except Notifications.DoesNotExist:
            return None, "Notificação não encontrada."

        notification.update(display=False)

        return notification, None
