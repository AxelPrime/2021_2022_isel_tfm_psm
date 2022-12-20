from rest_framework.serializers import *


class ReferPatientDataSerializer(Serializer):
    patient_name = CharField()
    patient_sns_number = CharField()
    patient_social_security_number = CharField()
    patient_phone_number = CharField()
    patient_birth_date = DateField(input_formats=["%d/%m/%Y"])
    patient_gender = CharField()
    patient_country = CharField()
    patient_nationality = CharField()
    patient_disease_type = CharField()
    patient_admission_diagnosis = CharField()
    patient_internment_duration = CharField()
    patient_next_of_kin_name = CharField(allow_null=True, allow_blank=True)
    patient_next_of_kin_kinship = CharField(allow_null=True, allow_blank=True)
    patient_next_of_kin_contact = CharField(allow_null=True, allow_blank=True)
    patient_internment_motive = CharField()
    patient_other_diagnosis = CharField(allow_null=True, allow_blank=True)
    patient_medication = CharField(allow_null=True, allow_blank=True)
    patient_supervision = CharField()
    patient_social_security_status = CharField()
    patient_social_status = CharField()
    patient_origin_institution = CharField()
    patient_doctor_name = CharField(allow_null=True, allow_blank=True)
    patient_doctor_professional_certificate = CharField(allow_null=True, allow_blank=True)
    patient_care_house = CharField()
    patient_address = CharField()
    patient_postal_code = CharField()
    patient_locality = CharField()
    patient_social_assistant = CharField()
    patient_subsystem = CharField()
    create_db = BooleanField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class ReferPatientFileSerializer(Serializer):
    patient_responsibility_term = FileField()
    patient_supervision_scale = FileField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass