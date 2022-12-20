from rest_framework.serializers import *


class FinalizeInvoiceDataSerializer(Serializer):
    invoice_number = IntegerField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class FinalizeInvoiceFileSerializer(Serializer):
    invoice_file = FileField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass