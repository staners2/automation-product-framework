from rest_framework import serializers

from product_app.models.EmployeesModel import EmployeesModel
from product_app.models.EventTypesModel import EventTypesModel
from product_app.models.EventsModel import EventsModel
from product_app.models.ProductsModel import ProductsModel


class UpdateEventsSerializer(serializers.ModelSerializer):

    date = serializers.DateField(required=True)
    type = serializers.PrimaryKeyRelatedField(queryset=EventTypesModel.objects, required=True, many=False)
    product = serializers.PrimaryKeyRelatedField(queryset=ProductsModel.objects, required=True, many=False)
    assignee = serializers.PrimaryKeyRelatedField(queryset=EmployeesModel.objects, required=True, many=False)
    url = serializers.URLField(required=False)

    class Meta:
        model = EventsModel
        fields = "__all__"

    # TODO: Добавить проверку на уникальность обновляемых событий у каждого продукта
    def validate(self, attrs):
        if (
            EventsModel.objects.exclude(id=self.instance.id)
            .filter(
                date=self.initial_data.get("date", self.instance.date),
                type=self.initial_data.get("type", self.instance.type.id),
                product=self.initial_data.get("product", self.instance.product.id),
                assignee=self.initial_data.get("assignee", self.instance.assignee.id),
                url=self.initial_data.get("url", self.instance.url),
            )
            .count()
            != 0
        ):
            raise serializers.ValidationError("Событие уже добавлено!")

        return attrs

    def update(self, instance, validated_data):
        instance.date = validated_data.get("date", instance.date)
        instance.type = validated_data.get("type", EventTypesModel.objects.get(id=instance.type.id))
        instance.product = validated_data.get("product", ProductsModel.objects.get(id=instance.product.id))
        instance.assignee = validated_data.get("assignee", EmployeesModel.objects.get(id=instance.assignee.id))
        instance.url = validated_data.get("url", instance.url)
        instance.description = validated_data.get("description", instance.description)
        instance.save()

        return instance
