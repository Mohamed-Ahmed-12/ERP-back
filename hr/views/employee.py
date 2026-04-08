from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from hr.models.employee import Employee
from hr.serializers.employee import EmployeeSerializer, EmployeeWriteSerializer

class EmployeeViewset(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    lookup_field = 'guid'
        
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return EmployeeWriteSerializer
        return EmployeeSerializer
    
    def get_queryset(self):
        return Employee.objects.select_related('position','department').all()
    
    @action(detail=False , methods=['get'])
    def dropdown(self, request):
        employees = self.get_queryset()
        data = [{'label': emp.first_name + ' ' + emp.last_name, 'value': emp.guid} for emp in employees]
        return Response(data=data  , status=status.HTTP_200_OK)
    
    
