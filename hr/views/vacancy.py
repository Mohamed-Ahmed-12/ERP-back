from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from hr.models.vacancy import Vacancy
from hr.serializers.vacancy import VacancyWriteSerializer, VacancyReadSerializer

class VacancyViewSet(viewsets.ModelViewSet):
    queryset = Vacancy.objects.all()
    lookup_field = 'guid'
        
    def get_queryset(self):
        return Vacancy.objects.select_related('position').all()
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return VacancyWriteSerializer
        return VacancyReadSerializer
    
    @action(detail=False, methods=['get'])
    def dropdown(self, request):
        vacancies = self.get_queryset()
        data = [{'label': vacancy.position.title, 'value': vacancy.guid} for vacancy in vacancies]
        return Response(data=data  , status=status.HTTP_200_OK)