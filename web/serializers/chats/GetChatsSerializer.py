from rest_framework import serializers

from web.models.ChatsModel import ChatsModel


class GetChatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatsModel
        exclude = ("updated", "deleted")
