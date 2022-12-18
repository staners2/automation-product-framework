from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from product_app.filters.PlansDateFilter import PlansDateFilter
from product_app.models import PlansModel
from product_app.serializers.plans.CreatePlansSerializer import CreatePlansSerializer
from product_app.serializers.plans.GetPlansSerializer import GetPlansSerializer
from product_app.serializers.plans.UpdatePlansSerializer import UpdatePlansSerializer


class PlansViewSets(ModelViewSet):  # viewsets.ViewSet
    # queryset = EventTypesModel.objects.all()
    serializer_class = GetPlansSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = []
    filterset_class = PlansDateFilter
    search_fields = []

    # override get queryset
    def get_queryset(self):
        return PlansModel.objects.all()


    def create(self, request, *args, **kwargs):
        serializer = CreatePlansSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = UpdatePlansSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
