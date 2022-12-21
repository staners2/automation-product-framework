from rest_framework import serializers

from product_app.models.PlansModel import PlansModel


class CreatePlansSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlansModel
        fields = "__all__"

    def validate_date(self, value):
        if PlansModel.objects.filter(product=self.initial_data["product"], date=self.initial_data["date"]).count() != 0:
            raise serializers.ValidationError("План на этот месяц уже составлен")

        return value
