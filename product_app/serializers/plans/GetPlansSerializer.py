from rest_framework import serializers

from product_app.models import PlansModel
from product_app.serializers.ProductsSerializer import ProductsSerializer


class GetPlansSerializer(serializers.ModelSerializer):

    product = ProductsSerializer(many=False)

    class Meta:
        model = PlansModel
        fields = "__all__"
