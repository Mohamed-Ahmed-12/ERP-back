from django.db import models
from core.models import BaseModel

class RequestStatusChoices(models.TextChoices):
    PENDING = 'Pending', 'Pending'
    APPROVED = 'Approved', 'Approved'
    REJECTED = 'Rejected', 'Rejected'

class JobChangeTypeChoices(models.TextChoices):
    PROMOTION = 'Promotion', 'Promotion'
    DEMOTION = 'Demotion', 'Demotion'
    TRANSFER = 'Transfer', 'Lateral Transfer'

class JobChangeRequest(BaseModel):
    employee = models.ForeignKey(
        'Employee', 
        on_delete=models.CASCADE, 
        related_name='job_change_requests'
    )
    request_type = models.CharField(
        max_length=20, 
        choices=JobChangeTypeChoices.choices,
        default=JobChangeTypeChoices.PROMOTION
    )
    
    current_position = models.ForeignKey(
        'JobPosition', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='current_position_changes'
    )
    
    desired_position = models.ForeignKey(
        'JobPosition', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='desired_position_changes'
    )
    
    reason = models.TextField(blank=True, null=True)
    
    status = models.CharField(
        max_length=20, 
        choices=RequestStatusChoices.choices,
        default=RequestStatusChoices.PENDING
    )

    class Meta:
        verbose_name = "Job Change Request"
        verbose_name_plural = "Job Change Requests"
        app_label = 'hr'

    def __str__(self):
        emp_name = f"{self.employee.first_name} {self.employee.last_name}"
        old_pos = self.current_position.title if self.current_position else 'N/A'
        new_pos = self.desired_position.title if self.desired_position else 'N/A'
        return f"{self.request_type} Request: {emp_name} ({old_pos} -> {new_pos})"
    
    def save(self, *args, **kwargs):
        # Auto-fill current position from employee profile if not provided
        if not self.current_position and self.employee and hasattr(self.employee, 'position'):
            self.current_position = self.employee.position
        super().save(*args, **kwargs)

    # Useful for the UI to show how long a request has been sitting
    @property
    def days_since_request(self):
        from django.utils import timezone
        delta = timezone.now() - self.created_at # Assuming BaseModel has created_at
        return delta.days