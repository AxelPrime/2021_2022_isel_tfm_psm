from rest_framework.serializers import *


class RegisterInternmentsSerializer(Serializer):
    referrals = ListField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass