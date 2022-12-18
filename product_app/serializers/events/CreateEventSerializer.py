from rest_framework import serializers

from product_app.models import EventsModel
from product_app.serializers.EventTypesSerializer import EventTypesSerializer
from product_app.serializers.ProductsSerializer import ProductsSerializer


class CreateEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventsModel
        fields = "__all__"

    def validate_url(self, value):
        if (
                EventsModel.objects.filter(
                    url=value, product=self.initial_data["product"], date=self.initial_data["date"]
                ).count()
                != 0
        ):
            raise serializers.ValidationError("Событие уже добавлено!")

        return value
