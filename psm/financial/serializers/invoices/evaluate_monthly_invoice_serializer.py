from rest_framework.serializers import *

EVALUATION_CHOICES = [
    ('true', 'True'),
    ('false', 'False'),
]


class EvaluateMonthlyInvoiceSerializer(Serializer):
    invoice_number = IntegerField()
    approve = ChoiceField(choices=EVALUATION_CHOICES)
    rejection_reason = CharField(allow_null=True, allow_blank=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
