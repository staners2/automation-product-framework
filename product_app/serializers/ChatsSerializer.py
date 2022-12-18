from rest_framework import serializers

from product_app.models.ChatsModel import ChatsModel


class ChatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatsModel
        fields = "__all__"
