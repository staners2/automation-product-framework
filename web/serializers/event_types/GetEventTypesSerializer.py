from rest_framework import serializers

from web.models.EventTypesModel import EventTypesModel


class GetEventTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventTypesModel
        exclude = ("updated", "deleted")
