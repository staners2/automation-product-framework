from rest_framework import serializers

from web.models.NamespacesModel import NamespacesModel


class GetNamespacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NamespacesModel
        exclude = ("updated", "deleted")
