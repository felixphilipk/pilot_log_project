from rest_framework import serializers
from .models import PilotLog

class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = PilotLog
        fields = "__all__"
