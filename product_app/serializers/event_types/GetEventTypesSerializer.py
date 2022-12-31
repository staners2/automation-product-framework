from rest_framework import serializers

from product_app.models.EventTypesModel import EventTypesModel


class GetEventTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventTypesModel
        exclude = ("updated", "deleted")
