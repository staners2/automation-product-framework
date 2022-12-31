from django.utils import timezone
from rest_framework import serializers

from web.models.EmployeesModel import EmployeesModel
from web.models.EventsModel import EventsModel
from web.models.EventTypesModel import EventTypesModel
from web.models.ProductsModel import ProductsModel


class UpdateEventsSerializer(serializers.ModelSerializer):

    date = serializers.DateField(required=False)
    type = serializers.PrimaryKeyRelatedField(
        queryset=EventTypesModel.objects.filter(deleted=None).all(),
        required=False,
        many=False,
    )
    product = serializers.PrimaryKeyRelatedField(
        queryset=ProductsModel.objects.filter(deleted=None).all(),
        required=False,
        many=False,
    )
    assignee = serializers.PrimaryKeyRelatedField(
        queryset=EmployeesModel.objects.filter(deleted=None).all(),
        required=False,
        many=False,
    )
    url = serializers.URLField(required=False)

    class Meta:
        model = EventsModel
        exclude = ("updated", "deleted")

    def validate(self, attrs):
        if (
            EventsModel.objects.exclude(id=self.instance.id)
            .filter(
                date=attrs.get("date", self.instance.date),
                type=attrs.get("type", self.instance.type.id),
                product=attrs.get("product", self.instance.product.id),
                assignee=attrs.get("assignee", self.instance.assignee.id),
                url=attrs.get("url", self.instance.url),
                deleted=None,
            )
            .count()
            != 0
        ):
            raise serializers.ValidationError("Такое событие уже существует!")

        return attrs

    def update(self, instance, validated_data):
        instance.date = validated_data.get("date", instance.date)
        instance.type = validated_data.get("type", EventTypesModel.objects.get(id=instance.type.id))
        instance.product = validated_data.get("product", ProductsModel.objects.get(id=instance.product.id))
        instance.assignee = validated_data.get("assignee", EmployeesModel.objects.get(id=instance.assignee.id))
        instance.url = validated_data.get("url", instance.url)
        instance.description = validated_data.get("description", instance.description)
        instance.updated = timezone.now()
        instance.save()

        return instance