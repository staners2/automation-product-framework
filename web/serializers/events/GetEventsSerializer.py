from rest_framework import serializers

from web.models.EventsModel import EventsModel
from web.serializers.employees.GetEmployeesSerializer import GetEmployeesSerializer
from web.serializers.event_types.GetEventTypesSerializer import GetEventTypesSerializer
from web.serializers.products.GetProductsSerializer import GetProductsSerializer


class GetEventsSerializer(serializers.ModelSerializer):

    date = serializers.DateField(required=True)
    type = GetEventTypesSerializer(many=False)
    product = GetProductsSerializer(many=False)
    assignee = GetEmployeesSerializer(many=False)

    class Meta:
        model = EventsModel
        exclude = ("updated", "deleted")
