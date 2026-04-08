from rest_framework import serializers

from hr.models.job_position import JobPosition
from hr.serializers.positions import JobPositionReadSerializer
from hr.models.vacancy import Vacancy
    
    
class VacancyReadSerializer(serializers.ModelSerializer):
    position = JobPositionReadSerializer(read_only=True)
    
    # Standardized output format for the frontend
    open_date = serializers.DateField(
        input_formats=["%Y-%m-%d", "iso-8601"],
    )
    close_date = serializers.DateField(
        input_formats=["%Y-%m-%d", "iso-8601"],
        allow_null=True,
        required=False
    )
    class Meta:
        model = Vacancy
        fields = '__all__'
        
class VacancyWriteSerializer(serializers.ModelSerializer):
    position = serializers.PrimaryKeyRelatedField(
        queryset=JobPosition.objects.all(),
    )
    open_date = serializers.DateField(
        input_formats=["%Y-%m-%d", "iso-8601"],
    )
    close_date = serializers.DateField(
        input_formats=["%Y-%m-%d", "iso-8601"],
        allow_null=True,
        required=False
    )

    class Meta:
        model = Vacancy
        fields = ['position', 'open_date', 'close_date' , 'number_of_positions', 'description', 'required_qualifications', 'responsibilities', 'is_open']