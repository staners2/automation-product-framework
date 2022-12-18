from rest_framework import serializers

from product_app.models import EventsModel
from product_app.serializers.EventTypesSerializer import EventTypesSerializer
from product_app.serializers.ProductsSerializer import ProductsSerializer


class EventsSerializer(serializers.ModelSerializer):

    # types = serializers.StringRelatedField(many=False)
    type = EventTypesSerializer(many=False, required=False)
    product = ProductsSerializer(many=False, required=False)

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

    # def get_product(self, instance):
    #     pass
    #
    # def get_type(self, instance):
    #     pass
