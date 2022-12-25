from rest_framework import serializers

from product_app.models.EventsModel import EventsModel

from product_app.serializers.employees.GetEmployeesSerializer import GetEmployeesSerializer
from product_app.serializers.event_types.GetEventTypesSerializer import GetEventTypesSerializer
from product_app.serializers.products.GetProductsSerializer import GetProductsSerializer


class GetEventsSerializer(serializers.ModelSerializer):

    date = serializers.DateField(required=True)
    type = GetEventTypesSerializer(many=False)
    product = GetProductsSerializer(many=False)
    assignee = GetEmployeesSerializer(many=False)

    class Meta:
        model = EventsModel
        fields = "__all__"
