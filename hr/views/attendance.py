from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from hr.models.attendance import Attendance
from hr.serializers.attendance import AttendanceReadSerializer, AttendanceWriteSerializer

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    lookup_field = 'guid'
    
    def get_queryset(self):
        return Attendance.objects.select_related('employee').all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return AttendanceWriteSerializer
        return AttendanceReadSerializer
    
    @action(detail=False, methods=['get'])
    def dropdown(self, request):
        attendances = self.get_queryset()
        data = [{'label': att.employee.first_name + ' ' + att.employee.last_name, 'value': att.guid} for att in attendances]
        return Response(data=data  , status=status.HTTP_200_OK)