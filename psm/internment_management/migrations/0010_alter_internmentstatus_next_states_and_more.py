# Generated by Django 4.0.3 on 2022-04-07 19:15

from django.db import migrations, models
import django_better_admin_arrayfield.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('internment_management', '0009_internmentstatus_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internmentstatus',
            name='next_states',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.CharField(max_length=25), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='internmentstatus',
            name='prev_states',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.CharField(max_length=25), blank=True, null=True, size=None),
        ),
    ]
