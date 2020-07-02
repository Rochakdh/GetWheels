from rest_framework.views import APIView
from rest_framework import viewsets,generics
from home.api.serializers import ItemSerializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from home.models import VehicleAvailable

class ItemFilterListView(generics.ListAPIView):
    serializer_class = ItemSerializers
    queryset = VehicleAvailable.objects.all()
    filter_backends = (DjangoFilterBackend,OrderingFilter,SearchFilter)
    filter_fields = ('type','manufacturer_company','model',)
    # search_fields = ('title','slug')