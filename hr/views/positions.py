from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from hr.models.job_position import JobPosition
from hr.serializers.positions import JobPositionReadSerializer, JobPositionWriteSerializer    

class JobPositionViewSet(viewsets.ModelViewSet):
    queryset = JobPosition.objects.all()
    lookup_field = 'guid'
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return JobPositionWriteSerializer
        return JobPositionReadSerializer
    
    def get_queryset(self):
        return JobPosition.objects.select_related('department').all()
    
        
    @action(detail=False , methods=['get'])
    def dropdown(self, request):
        positions = self.get_queryset()
        data = [{'label': pos.title, 'value': pos.guid} for pos in positions]
        return Response(data=data  , status=status.HTTP_200_OK)
