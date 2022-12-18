from rest_framework import serializers

from product_app.models.EventsModel import EventsModel


class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventsModel
        fields = "__all__"

    # TODO: Добавить проверку на уникальность обновляемых событий у каждого продукта
    def validate_url(self, value):
        if (
            EventsModel.objects.filter(
                url=value, product=self.initial_data["product"], date=self.initial_data["date"]
            ).count()
            != 0
        ):
            raise serializers.ValidationError("Событие уже добавлено!")

        return value
