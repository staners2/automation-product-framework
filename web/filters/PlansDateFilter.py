from django_filters import DateFilter, FilterSet

from web.models.PlansModel import PlansModel


class PlansDateFilter(FilterSet):
    date_start = DateFilter(field_name="date", lookup_expr="gte")
    date_end = DateFilter(field_name="date", lookup_expr="lte")

    class Meta:
        model = PlansModel
        fields = ("date_start", "date_end")
