from rest_framework import serializers

from product_app.models.NamespacesModel import NamespacesModel


class GetNamespacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NamespacesModel
        fields = "__all__"
