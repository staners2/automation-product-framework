from decimal import Decimal

from django.core.validators import MinValueValidator
from rest_framework import serializers
from datetime import date

from product_app.models.PlansModel import PlansModel
from product_app.serializers.products.GetProductsSerializer import GetProductsSerializer


class UpdatePlansSerializer(serializers.ModelSerializer):

    product = GetProductsSerializer(required=False, many=False)
    date = serializers.DateField(required=False)
    daily = serializers.DecimalField(
        decimal_places=2,
        max_digits=5,
        validators=[MinValueValidator(Decimal("0"))],
        required=False
    )
    review_code = serializers.DecimalField(
        decimal_places=2,
        max_digits=5,
        validators=[MinValueValidator(Decimal("0"))],
        required=False
    )
    one_to_one = serializers.DecimalField(
        decimal_places=2,
        max_digits=5,
        validators=[MinValueValidator(Decimal("0"))],
        required=False,
    )
    individual_plan = serializers.DecimalField(
        decimal_places=2,
        max_digits=5,
        validators=[MinValueValidator(Decimal("0"))],
        required=False,
    )
    meeting_on_product = serializers.DecimalField(
        decimal_places=2,
        max_digits=5,
        validators=[MinValueValidator(Decimal("0"))],
        required=False,
    )
    close_task = serializers.DecimalField(
        decimal_places=2,
        max_digits=5,
        validators=[MinValueValidator(Decimal("0"))],
        required=False,
    )

    class Meta:
        model = PlansModel
        fields = "__all__"

    def validate_date(self, value):
        # print(self.instance.__dict__)
        # print(self.initial_data)
        # if (PlansModel.objects.filter(product=self.initial_data["product"], date=self.initial_data["date"], id=self.instance.id).count() != 0):
        #     raise serializers.ValidationError("План на этот месяц уже составлен")

        return value
