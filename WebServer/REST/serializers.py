from rest_framework import serializers

from .models import *


class VehicleSerializer(serializers.ModelSerializer):
    """
    Serializer for the Vehicle model.
    """

    class Meta:
        model = Vehicle
        fields = ['id', 'latitude', 'longitude', 'smoke', 'temperature', "humidity"]


class AlertSerializer(serializers.ModelSerializer):
    """
    Serializer for the Alert model.
    """

    class Meta:
        model = Alert
        fields = ['sender', 'latitude', 'longitude', 'smoke', 'temperature', "s", "t", "u", "humidity"]
        # Include only the specified fields of the Alert model
