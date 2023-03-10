# Generated by Django 4.0.3 on 2022-04-02 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CareHouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identification_code', models.CharField(max_length=25, unique=True)),
                ('name', models.CharField(max_length=128)),
                ('address', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='MedicalInstitution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institution_code', models.CharField(max_length=25, unique=True)),
                ('name', models.CharField(max_length=128)),
                ('address', models.CharField(max_length=256)),
                ('nif', models.CharField(max_length=9, unique=True)),
            ],
        ),
    ]
