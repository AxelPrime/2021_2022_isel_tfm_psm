from django.db import models

from user_management.models import CustomUser
from .patient import Patient
from .internment_status import InternmentStatus
from entities.models import MedicalInstitution, CareHouse
from ..utils.referral_files_path import referral_files_path


class Referral(models.Model):
    # The possible supervision levels.
    supervision_choices = [
        ("1", "Sem/Pouca Supervisão"),
        ("2", "Bastante/Muita Supervisão"),
        ("3", "Alta Supervisão"),
    ]

    # The possible internment duration choices.
    internment_duration_choices = [
        ('short', 'Curta Duração'),
        ('medium', 'Média Duração'),
        ('long', 'Longa Duração'),
    ]

    # The available typology choices.
    typology_choices = [
        ("I", "I"),
        ("II", "II"),
        ("III", "III"),
    ]

    # The possible choices for the disease type.
    disease_type_choices = [
        ('1', '1 - Rabilitação'),
        ('2', '2 - Alcoologia'),
        ('3', '3 - Agudos'),
        ('4', '4 - Psicogeriatria'),
        ('5', '5 - Psiquiatria Longa Duração'),
    ]

    # The identifier of the referral.
    identifier = models.CharField(max_length=64, unique=True)
    # The patient that is referred.
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    # The origin institution.
    origin_institution = models.ForeignKey(MedicalInstitution, on_delete=models.CASCADE)
    # The Care House that this patient is being referred to.
    care_house = models.ForeignKey(CareHouse, on_delete=models.CASCADE)
    # The typology of the referral.
    typology = models.CharField(max_length=3, choices=typology_choices)
    # The admission diagnosis.
    admission_diagnosis = models.CharField(max_length=256)
    # The type of disease.
    disease_type = models.CharField(max_length=1, choices=disease_type_choices)
    # The process' number.
    process_number = models.CharField(max_length=25, unique=True)
    # The responsibility term.
    responsibility_term = models.FileField(upload_to=referral_files_path)
    # The patient supervision scale.
    supervision_scale = models.FileField(upload_to=referral_files_path)
    # The patients' family situation.
    family_situation = models.CharField(max_length=256)
    # The relative name.
    relative_name = models.CharField(max_length=256, null=True, blank=True)
    # The relative kinship.
    relative_kinship = models.CharField(max_length=256, null=True, blank=True)
    # The relative contact.
    relative_contact = models.CharField(max_length=256, null=True, blank=True)
    # The social assistant of the patient.
    social_assistant = models.CharField(max_length=256, null=True, blank=True)
    # The supervision grade.
    supervision_grade = models.CharField(max_length=2, choices=supervision_choices)
    # The referral motive.
    referral_motive = models.TextField()
    # Other diagnosis of the patients.
    other_diagnosis = models.TextField(blank=True)
    # The patient's social situation.
    social_situation = models.CharField(max_length=256)
    # The internment duration.
    internment_duration = models.CharField(max_length=25, choices=internment_duration_choices)
    # The Patients medication.
    medication = models.TextField()
    # The referral's date.
    referral_date = models.DateTimeField()
    # The date of the approval.
    approval_date = models.DateTimeField(null=True)
    # The current status.
    current_status = models.ForeignKey(InternmentStatus, on_delete=models.CASCADE)
    # The user who made the referral.
    referred_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # The name of the doctor that referenced the patient.
    doctor_name = models.CharField(max_length=128)
    # The professional certificate of the doctor.
    doctor_professional_certificate = models.CharField(max_length=20)
    # The rejection reason for the referral.
    rejection_reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.patient.name
