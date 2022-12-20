from django.db import models


class NotificationTemplate(models.Model):
    # The identifier of this template.
    identifier = models.CharField(max_length=50, unique=True)
    # The template content.
    text = models.TextField()
    # The icon to be used.
    icon = models.CharField(max_length=30)
    # The background color of the icon.
    bg_color = models.CharField(max_length=30)

    def __str__(self):
        return self.identifier
