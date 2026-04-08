from rest_framework import serializers
from hr.models.department import Department
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['guid', 'name', 'description', 'created_at', 'updated_at']