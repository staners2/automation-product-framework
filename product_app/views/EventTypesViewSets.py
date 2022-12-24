from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from product_app.models.EventTypesModel import EventTypesModel
from product_app.serializers.EventTypesSerializer import EventTypesSerializer


class EventTypesViewSets(ModelViewSet):
    serializer_class = EventTypesSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["point"]
    search_fields = [""]

    # override get queryset
    def get_queryset(self):
        return EventTypesModel.objects.all()
