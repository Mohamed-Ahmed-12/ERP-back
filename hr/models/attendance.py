from django.db import models
from core.models import BaseModel


class AttendanceStatusChoices(models.TextChoices):
    PRESENT = 'Present', 'Present'
    ABSENT = 'Absent', 'Absent'
    LATE = 'Late', 'Late'
    ON_LEAVE = 'On Leave', 'On Leave'
    
class Attendance(BaseModel):
    employee = models.ForeignKey(
        'Employee', 
        on_delete=models.CASCADE, 
        related_name='attendance_records'
    )
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, blank=True, null=True , choices=AttendanceStatusChoices.choices)
    shift_type = models.CharField(max_length=20, choices=[('Day', 'Day'), ('Night', 'Night')], null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Attendance Record'
        verbose_name_plural = 'Attendance Records'
        app_label = 'hr'
        
    @property
    def total_hours(self):
        if self.check_in_time and self.check_out_time:
            delta = self.check_out_time - self.check_in_time
            return delta.total_seconds() / 3600  # Convert to hours
        return 0
    
    def __str__(self):
        return f"Attendance for {self.employee.first_name} {self.employee.last_name} on {self.check_in_time.date()}"
 