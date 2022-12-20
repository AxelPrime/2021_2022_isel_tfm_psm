from user_management.models import NotificationTemplate


def run():
    # Define the list of templates to create.
    template_list = [
        {
            "identifier": "REFERRAL_CREATION",
            "text": "Foi criada uma nova referenciação.",
            "icon": "bi bi-file-earmark",
            "bg_color": "bg-primary"
        },
        {
            "identifier": "REFERRAL_OPENING_AVAILABLE",
            "text": "Existe uma vaga aberta para uma referenciação.",
            "icon": "bi bi-file-earmark",
            "bg_color": "bg-success"
        },
        {
            "identifier": "REFERRAL_OPENING_UNAVAILABLE",
            "text": "Não existe vaga para uma referenciação.",
            "icon": "bi bi-file-earmark",
            "bg_color": "bg-danger"
        },
        {
            "identifier": "REFERRAL_APPROVED",
            "text": "Foi aprovada uma referenciação.",
            "icon": "bi bi-file-earmark",
            "bg_color": "bg-success"
        },
        {
            "identifier": "REFERRAL_REJECTED",
            "text": "Foi rejeitada uma referenciação.",
            "icon": "bi bi-file-earmark",
            "bg_color": "bg-danger"
        },
    ]

    # Iterate the template list.
    for template in template_list:
        NotificationTemplate.objects.get_or_create(**template)
