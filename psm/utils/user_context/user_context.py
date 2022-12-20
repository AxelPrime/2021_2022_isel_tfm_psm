from django.db.models import Q

from user_management.models import CustomUser, Notifications


def get_user_context(user: CustomUser):
    notifications_query = Q(user_type=user.user_type) & Q(display=True)
    if user.user_type == "care_house_staff":
        notifications_query &= Q(care_house=user.care_house)
    notifications = [
        {
            "id": n.identifier,
            "readable": n.readable_on_click,
            "link": n.redirect_to,
            "text": n.template.text,
            "title": n.get_process_type_display(),
            "icon": n.template.icon,
            "bg": n.template.bg_color,
            "date": n.created.strftime("%d/%m/%Y"),
        }
        for n in Notifications.objects.filter(notifications_query)
    ]

    return {
        'name': f"{user.first_name} {user.last_name}",
        'user_type': user.user_type,
        'user_type_name': user.get_user_type_display(),
        'notification_data': {
            "count": len(notifications),
            "notifications": notifications,
        }
    }
