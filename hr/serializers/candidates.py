from rest_framework import serializers
from hr.models.candidate import Candidate
from hr.models.vacancy import Vacancy
from hr.serializers.vacancy import VacancyReadSerializer

class CandidateReadSerializer(serializers.ModelSerializer):
    vacancy = VacancyReadSerializer(read_only=True)
    class Meta:
        model = Candidate
        fields = '__all__'
        
class CandidateWriteSerializer(serializers.ModelSerializer):
    vacancy = serializers.PrimaryKeyRelatedField(queryset=Vacancy.objects.all())
    class Meta:
        model = Candidate
        fields = '__all__'