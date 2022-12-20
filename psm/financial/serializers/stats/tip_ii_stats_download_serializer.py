from rest_framework.serializers import *


class TipIIStatsDownloadSerializer(Serializer):
    year = IntegerField()
    month = IntegerField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
