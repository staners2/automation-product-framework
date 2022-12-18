from rest_framework import serializers

from product_app.models.EventsModel import EventsModel
from product_app.serializers.EventTypesSerializer import EventTypesSerializer
from product_app.serializers.ProductsSerializer import ProductsSerializer


class GetEventsSerializer(serializers.ModelSerializer):

    # types = serializers.StringRelatedField(many=False)
    type = EventTypesSerializer(many=False, required=False)
    product = ProductsSerializer(many=False, required=False)

    class Meta:
        model = EventsModel
        fields = "__all__"
