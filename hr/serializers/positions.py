from rest_framework import serializers
from hr.models.job_position import JobPosition
from hr.serializers.departments import DepartmentSerializer
from rest_framework import serializers
from hr.models.department import Department

class JobPositionReadSerializer(serializers.ModelSerializer):
    # Full nested object for the UI
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = JobPosition
        fields = [
            'guid', 'title', 'department', 'contract_type', 
            'base_salary', 'created_at', 'updated_at','seniority_level'
        ]
        
class JobPositionWriteSerializer(serializers.ModelSerializer):
    # Use the GUID to link the department
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
    )

    class Meta:
        model = JobPosition
        fields = [
            'title', 'department', 'contract_type', 'base_salary','seniority_level'
        ]