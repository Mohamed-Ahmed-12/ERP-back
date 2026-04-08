from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from hr.models.job_change_request import JobChangeRequest
from hr.serializers.job_change_req import JobChangeReadSerializer , JobChangeWriteSerializer
class JobChangeRequestView(viewsets.ModelViewSet):
    queryset = JobChangeRequest.objects.all()
    lookup_field = 'guid'
        
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return JobChangeWriteSerializer
        return JobChangeReadSerializer
    
    def get_queryset(self):
        return JobChangeRequest.objects.select_related('current_position' , 'desired_position' , 'employee').all()
    
    @action(detail=False , methods=['get'])
    def dropdown(self, request):
        reqs = self.get_queryset()
        data = [{'label': req.employee.first_name + ' ' + req.employee.last_name , 'value': req.guid} for req in reqs]
        return Response(data=data  , status=status.HTTP_200_OK)