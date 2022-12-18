from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from product_app.filters.EventsDateFilter import EventsDateFilter
from product_app.models import EventsModel
from product_app.serializers.EventsSerializer import EventsSerializer


class EventsViewSets(ModelViewSet):  # viewsets.ViewSet
    # queryset = EventTypesModel.objects.all()
    serializer_class = EventsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = []
    filterset_class = EventsDateFilter
    search_fields = ["product", "type"]

    # override get queryset
    def get_queryset(self):
        return EventsModel.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
