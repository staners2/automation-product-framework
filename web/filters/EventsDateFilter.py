from django_filters import DateFilter, FilterSet

from web.models.EventsModel import EventsModel


class EventsDateFilter(FilterSet):
    date_start = DateFilter(field_name="date", lookup_expr="gte")
    date_end = DateFilter(field_name="date", lookup_expr="lte")

    class Meta:
        model = EventsModel
        fields = ("date_start", "date_end")
