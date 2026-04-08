from rest_framework import serializers
from django.utils import timezone

from hr.models.attendance import Attendance
from hr.serializers.employee import EmployeeBasicSerializer
from hr.models.employee import Employee

class AttendanceReadSerializer(serializers.ModelSerializer):
    # Full nested details for the UI (Name, ID, Photo, etc.)
    employee = EmployeeBasicSerializer(read_only=True)
    
    # Standardized output format for the frontend
    check_in = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", source='check_in_time')
    check_out = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", source='check_out_time')

    class Meta:
        model = Attendance
        fields = ['guid', 'employee', 'status', 'check_in', 'check_out' , 'shift_type']
        
class AttendanceWriteSerializer(serializers.ModelSerializer):
    # We only need the GUID to link the record
    employee = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all()
    )
    
    check_in = serializers.DateTimeField(
        input_formats=["%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M", "iso-8601"],
        source='check_in_time'
    )
    
    check_out = serializers.DateTimeField(
        input_formats=["%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M", "iso-8601"],
        source='check_out_time',
        allow_null=True,
        required=False
    )

    class Meta:
        model = Attendance
        fields = ['employee', 'status', 'check_in', 'check_out', 'shift_type']

    def validate(self, data):
        # 1. Extract data (using 'source' names from your field definitions)
        check_in = data.get('check_in_time')
        check_out = data.get('check_out_time')
        
        # FIX: Get employee immediately and handle the fallback for updates
        employee = data.get('employee') or (self.instance.employee if self.instance else None)

        if not employee:
            raise serializers.ValidationError({"employee": "Employee context is missing."})

        # 2. Prevent multiple "Open" sessions (Only on Creation)
        # We check if there is a record with no check_out_time
        if not self.instance:
            active_session = Attendance.objects.filter(
                employee=employee, 
                check_out_time__isnull=True
            ).exists()
            
            if active_session:
                raise serializers.ValidationError(
                    "This employee already has an active session. Please check-out before checking in again."
                )

        # 3. Chronological Check
        if check_in and check_out and check_out <= check_in:
            raise serializers.ValidationError({
                "check_out": "Check-out must be after check-in."
            })

        # 4. Future Date Check
        # Ensure they aren't checking in for a time that hasn't happened yet
        if check_in and check_in > timezone.now():
            raise serializers.ValidationError({
                "check_in": "Cannot record attendance for a future time."
            })

        # 5. Advanced Overlap Check
        # This prevents overlapping with CLOSED sessions or other open sessions
        if check_in:
            # If no check_out is provided (open session), we check against 'now'
            effective_end = check_out if check_out else timezone.now()
            
            overlap_query = Attendance.objects.filter(
                employee=employee,
                check_in_time__lt=effective_end,
                check_out_time__gt=check_in
            )
            
            if self.instance:
                overlap_query = overlap_query.exclude(pk=self.instance.pk)
            
            if overlap_query.exists():
                raise serializers.ValidationError(
                    "This time range overlaps with an existing attendance record."
                )

        return data