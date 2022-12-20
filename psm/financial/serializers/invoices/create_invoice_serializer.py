from rest_framework.serializers import *


class CreateInvoiceSerializer(Serializer):
    typology = CharField()
    dates_encrypted = CharField()
    care_house = CharField(allow_null=True, allow_blank=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
