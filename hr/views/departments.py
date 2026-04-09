from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from hr.models.department import Department
from hr.serializers.departments import DepartmentSerializer
from core.views import BaseViewSet

class DepartmentViewSet(BaseViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    lookup_field = 'guid'

    
    @action(detail=False, methods=['get'])
    def dropdown(self, request):
        departments = self.get_queryset()
        data = [{'label': dept.name, 'value': dept.guid} for dept in departments]
        return Response(data=data  , status=status.HTTP_200_OK)