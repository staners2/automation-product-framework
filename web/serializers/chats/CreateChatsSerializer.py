from rest_framework import serializers

from web.models.ChatsModel import ChatsModel


class CreateChatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatsModel
        exclude = ("updated", "deleted")

    # TODO: Валидацию на уникальность имен чатов и их chat_id
    # TODO: При валидации chat_id отправлять тестовое сообщение в указанный чат и удалять его (если дошло)?
    def validate_title(self, value):
        if (
            ChatsModel.objects.filter(
                title=value,
                deleted=None,
            ).count()
            != 0
        ):
            raise serializers.ValidationError("Чат с таким названием уже существует!")

        return value

    def validate_chat_id(self, value):
        if (
            ChatsModel.objects.filter(
                deleted=None,
                chat_id=value,
            ).count()
            != 0
        ):
            raise serializers.ValidationError("Чат с таким ID уже существует!")

        return value

    def create(self, validated_data):
        title = validated_data.get("title")
        chat_id = validated_data.get("chat_id")
        instance = ChatsModel(
            title=title,
            chat_id=chat_id,
        )
        instance.save()
        return instance
