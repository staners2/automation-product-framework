from django.utils import timezone
from rest_framework import serializers

from web.models.EmployeesModel import EmployeesModel


class UpdateEmployeesSerializer(serializers.ModelSerializer):

    login = serializers.CharField(required=False)

    class Meta:
        model = EmployeesModel
        exclude = ("updated", "deleted")

    def validate(self, attrs):
        if (
            EmployeesModel.objects.exclude(id=self.instance.id)
            .filter(
                login=attrs.get("login", self.instance.login),
                deleted=None,
            )
            .count()
            != 0
        ):
            raise serializers.ValidationError("Пользователь с таким логином уже существует!")

        return attrs

    def update(self, instance, validated_data):
        instance.login = validated_data.get("login", instance.login)
        instance.full_name = validated_data.get("full_name", instance.full_name)
        instance.updated = timezone.now()
        instance.save()

        return instance
