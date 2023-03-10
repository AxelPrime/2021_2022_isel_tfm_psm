# Generated by Django 4.0.3 on 2022-07-18 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0008_alter_notifications_notification_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='identifier',
            field=models.CharField(default='a', max_length=64, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notifications',
            name='readable_on_click',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='notifications',
            name='redirect_to',
            field=models.CharField(default='/', max_length=256),
            preserve_default=False,
        ),
    ]
