from rest_framework import serializers

from product_app.models.EventsModel import EventsModel


class UpdateEventsSerializer(serializers.ModelSerializer):

    date = serializers.DateField(required=False)
    type = serializers.IntegerField(required=False)
    product = serializers.IntegerField(required=False)

    class Meta:
        model = EventsModel
        fields = "__all__"

    # TODO: Добавить проверку на уникальность обновляемых событий у каждого продукта
    def validate_url(self, value):
        # if self.instance.id !=
        print(self.instance.__dict__)
        # if (
        #     EventsModel.objects.filter(
        #         url=value, product=self.initial_data["product"], date=self.initial_data["date"]
        #     ).count()
        #     != 0
        # ):
        #     raise serializers.ValidationError("Событие уже добавлено!")

        return value

    def validate(self, data):
        print(f"Start validate: {data}")
        return data
