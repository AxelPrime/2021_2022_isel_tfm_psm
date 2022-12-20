from rest_framework.serializers import *


class TypologyStatsSerializer(Serializer):
    year = IntegerField()
    month = IntegerField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
