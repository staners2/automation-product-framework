from rest_framework import serializers

from product_app.models.EventsModel import EventsModel
from product_app.serializers.EmployeesSerializer import EmployeesSerializer
from product_app.serializers.EventTypesSerializer import EventTypesSerializer
from product_app.serializers.products.ProductsSerializer import ProductsSerializer
from product_framework import settings


class GetEventsSerializer(serializers.ModelSerializer):

    date = serializers.DateField(required=True)
    type = EventTypesSerializer(many=False)
    product = ProductsSerializer(many=False)
    assignee = EmployeesSerializer(many=False)

    class Meta:
        model = EventsModel
        fields = "__all__"
