from rest_framework.serializers import *


class EvaluateReferralSerializer(Serializer):
    status = CharField()
    referrals = ListField()
    rejection_reason = CharField(allow_null=True, allow_blank=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
