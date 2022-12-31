from rest_framework import serializers

from product_app.models.ChatsModel import ChatsModel


class CreateChatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatsModel
        exclude = ("updated", "deleted")

    # TODO: Валидацию на уникальность имен чатов и их chat_id
    def validate(self, attrs):
        if (
            ChatsModel.objects.filter(title=self.initial_data["title"], chat_id=self.initial_data["chat_id"]).count()
            != 0
        ):
            raise serializers.ValidationError("Такой чат уже существует!")

        return attrs

    def create(self, validated_data):
        title = validated_data.get("title")
        chat_id = validated_data.get("chat_id")
        instance = ChatsModel(
            title=title,
            chat_id=chat_id,
        )
        instance.save()
        return instance
