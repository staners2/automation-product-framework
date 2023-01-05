from rest_framework import serializers

from web.models.PlansModel import PlansModel
from web.models.ProductsModel import ProductsModel


class CreatePlansSerializer(serializers.ModelSerializer):

    product = serializers.PrimaryKeyRelatedField(
        queryset=ProductsModel.objects.filter(deleted=None).all(),
        required=True,
        many=False,
    )

    class Meta:
        model = PlansModel
        exclude = ("updated", "deleted")

    # TODO: Сделать проверку формата даты записи только на 1 число каждого месяца
    def validate_date(self, value):
        if (
            PlansModel.objects.filter(
                product=self.initial_data.get("product"),
                date=self.initial_data.get("date"),
                deleted=None,
            ).count()
            != 0
        ):
            raise serializers.ValidationError("План на этот месяц уже составлен")

        return value

    def create(self, validated_data):
        date = validated_data.get("date")
        product = validated_data.get("product")
        daily = validated_data.get("daily", 0.0)
        review_code = validated_data.get("review_code", 0.0)
        one_to_one = validated_data.get("one_to_one", 0.0)
        individual_plan = validated_data.get("individual_plan", 0.0)
        meeting_on_product = validated_data.get("meeting_on_product", 0.0)
        close_task = validated_data.get("close_task", 0.0)
        instance = PlansModel(
            date=date,
            product=product,
            daily=daily,
            review_code=review_code,
            one_to_one=one_to_one,
            individual_plan=individual_plan,
            meeting_on_product=meeting_on_product,
            close_task=close_task,
        )
        instance.save()
        return instance
