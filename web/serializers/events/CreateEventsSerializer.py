from rest_framework import serializers

from web.models.EmployeesModel import EmployeesModel
from web.models.EventsModel import EventsModel
from web.models.EventTypesModel import EventTypesModel
from web.models.ProductsModel import ProductsModel


class CreateEventsSerializer(serializers.ModelSerializer):

    date = serializers.DateField(required=True)
    type = serializers.PrimaryKeyRelatedField(queryset=EventTypesModel.objects, many=False)
    product = serializers.PrimaryKeyRelatedField(queryset=ProductsModel.objects, many=False)
    assignee = serializers.PrimaryKeyRelatedField(queryset=EmployeesModel.objects, allow_null=True, many=False)

    class Meta:
        model = EventsModel
        exclude = ("updated", "deleted")

    def validate(self, attrs):
        print(self.initial_data)  # TODO: Вхождение всех 5 проверять
        if all(x in [key for key in self.initial_data] for x in ["product", "type", "assignee", "date", "url"]):
            if (
                EventsModel.objects.filter(
                    date=self.initial_data["date"],
                    product=self.initial_data["product"],
                    type=self.initial_data["type"],
                    assignee=self.initial_data["assignee"],
                    url=self.initial_data["url"],
                ).count()
                != 0
            ):
                raise serializers.ValidationError("Событие уже добавлено!")

        return attrs

    def create(self, validated_data):
        date = validated_data.get("date")
        type = validated_data.get("type")
        product = validated_data["product"]
        assignee = validated_data.get("assignee", None)
        url = validated_data.get("url")
        description = validated_data.get("description", None)
        instance = EventsModel(
            type=type,
            product=product,
            assignee=assignee,
            date=date,
            url=url,
            description=description,
        )
        instance.save()
        return instance
