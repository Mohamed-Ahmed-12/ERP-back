 
from django.db import models
from core.models import BaseModel


class RequestStatusChoices(models.TextChoices):
    PENDING = 'Pending', 'Pending'
    APPROVED = 'Approved', 'Approved'
    REJECTED = 'Rejected', 'Rejected'
       
class LeaveRequest(BaseModel):
    employee = models.ForeignKey(
        'Employee', 
        on_delete=models.CASCADE, 
        related_name='leave_requests'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    
    reason = models.TextField(blank=True, null=True)
    
    status = models.CharField(
        max_length=20, 
        choices=RequestStatusChoices.choices,
        default=RequestStatusChoices.PENDING
    )

    def __str__(self):
        return f"Leave Request for {self.employee.first_name} {self.employee.last_name} from {self.start_date} to {self.end_date}"
    class Meta:
        verbose_name = 'Leave Request'
        verbose_name_plural = 'Leave Requests'
        app_label = 'hr'