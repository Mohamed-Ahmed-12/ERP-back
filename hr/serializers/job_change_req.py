from rest_framework import serializers
from hr.models.job_change_request import JobChangeRequest , RequestStatusChoices
from hr.models.employee import Employee 
from hr.models.job_position import JobPosition
from hr.serializers.employee import EmployeeBasicSerializer
from hr.serializers.positions import JobPositionReadSerializer

class JobChangeReadSerializer(serializers.ModelSerializer):
    employee = EmployeeBasicSerializer(read_only=True)
    current_position = JobPositionReadSerializer(read_only=True)
    desired_position = JobPositionReadSerializer(read_only=True)
    
    class Meta:
        model = JobChangeRequest
        fields = ['guid','employee' , 'request_type' , 'current_position' , 'desired_position' , 'reason' , 'status']

class JobChangeWriteSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(
        queryset = Employee.objects.all()
    )
    current_position = serializers.PrimaryKeyRelatedField(
        queryset = JobPosition.objects.all()
    )
    desired_position = serializers.PrimaryKeyRelatedField(
        queryset = JobPosition.objects.all()
    )
    
    class Meta:
        model = JobChangeRequest
        fields = ['employee' , 'request_type' , 'current_position' , 'desired_position' , 'reason' , 'status']
    
    def validate(self, data):
        employee = data.get('employee')
        current_pos = data.get('current_position')
        desired_pos = data.get('desired_position')
        request_type = data.get('request_type')

        # Fallback for partial updates (PATCH)
        if self.instance:
            employee = employee or self.instance.employee
            current_pos = current_pos or self.instance.current_position
            desired_pos = desired_pos or self.instance.desired_position

        # 1. Logic Check: Current vs Desired
        if current_pos == desired_pos:
            raise serializers.ValidationError({
                "desired_position": "Desired position must be different from the current position."
            })

        # 2. Prevent Duplicate Pending Requests
        # We don't want the same employee spamming 'Promotion' requests for the same role
        existing_request = JobChangeRequest.objects.filter(
            employee=employee,
            desired_position=desired_pos,
            status=RequestStatusChoices.PENDING
        )
        
        if self.instance:
            existing_request = existing_request.exclude(pk=self.instance.pk)

        if existing_request.exists():
            raise serializers.ValidationError(
                f"There is already a pending {request_type} request for this position."
            )

        return data