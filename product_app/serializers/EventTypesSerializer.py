from rest_framework import serializers

from product_app.models.EventTypesModel import EventTypesModel


class EventTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventTypesModel
        fields = "__all__"
