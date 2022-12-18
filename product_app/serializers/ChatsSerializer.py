from rest_framework import serializers

from product_app.models import NamespacesModel


class ChatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NamespacesModel
        fields = "__all__"
