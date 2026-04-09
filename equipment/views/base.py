from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from core.views import BaseViewSet

from equipment.models import EquipmentType , EquipmentBrand , Equipment , EquipmentEmployee
from equipment.serializers.base import \
    EquipmentTypeSerializer , EquipmentReadSerializer , EquipmentWriteSerializer , EquipmentBrandSerializer , EquipmentEmployeeSerializer
from core.mixins import ApiResponseMixin


class EquipmentTypeViewSet(BaseViewSet):
    queryset = EquipmentType.objects.all()
    serializer_class = EquipmentTypeSerializer
    lookup_field = 'guid'
    
    @action(detail=False , methods=['get'])
    def dropdown(self, request):
        types = self.get_queryset()
        data = [{'label': t.name, 'value': t.guid} for t in types]
        return Response(data=data  , status=status.HTTP_200_OK)

class EquipmentBrandViewSet(BaseViewSet):
    queryset = EquipmentBrand.objects.all()
    serializer_class = EquipmentBrandSerializer
    lookup_field = 'guid'
    
    @action(detail=False , methods=['get'])
    def dropdown(self, request):
        brands = self.get_queryset()
        data = [{'label': brand.name, 'value': brand.guid} for brand in brands]
        return Response(data=data  , status=status.HTTP_200_OK)

class EquipmentViewSet(BaseViewSet):
    queryset = Equipment.objects.all()
    lookup_field = 'guid'
    
    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return EquipmentWriteSerializer
        return EquipmentReadSerializer
    
    @action(detail=False , methods=['get'])
    def dropdown(self, request):
        equipments = self.get_queryset()
        data = [{'label': eq.name, 'value': eq.guid} for eq in equipments]
        return Response(data=data  , status=status.HTTP_200_OK)
    
class EquipmentEmployeeViewSet(BaseViewSet):
    queryset = EquipmentEmployee.objects.all()
    serializer_class = EquipmentEmployeeSerializer
    lookup_field = 'guid'
    
    @action(detail=False , methods=['get'])
    def dropdown(self, request):
        employees = self.get_queryset()
        data = [{'label': e.first_name + " " + e.last_name , 'value': e.guid} for e in employees]
        return Response(data=data  , status=status.HTTP_200_OK)
    