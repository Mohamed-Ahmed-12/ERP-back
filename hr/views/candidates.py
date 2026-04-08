from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from hr.models.candidate import Candidate

from hr.serializers.candidates import CandidateReadSerializer, CandidateWriteSerializer

class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    # parser_classes = (MultiPartParser, FormParser)
    lookup_field = 'guid'

        
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CandidateWriteSerializer
        return CandidateReadSerializer
    
    def get_queryset(self):
        return Candidate.objects.select_related('vacancy').all()
    
    @action(detail=False , methods=['get'])
    def dropdown(self, request):
        candidates = self.get_queryset()
        data = [{'label': cand.first_name + ' ' + cand.last_name, 'value': cand.guid} for cand in candidates]
        return Response(data=data  , status=status.HTTP_200_OK)
    
    
