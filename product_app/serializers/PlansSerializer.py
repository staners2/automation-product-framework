from rest_framework import serializers

from product_app.models import PlansModel


class PlansSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlansModel
        fields = "__all__"
