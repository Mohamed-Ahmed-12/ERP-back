 
from django.db import models
from core.models import BaseModel

class RequestStatusChoices(models.TextChoices):
    PENDING = 'Pending', 'Pending'
    APPROVED = 'Approved', 'Approved'
    REJECTED = 'Rejected', 'Rejected'
    
class SalaryIncreaseRequest(BaseModel):
    employee = models.ForeignKey(
        'Employee', 
        on_delete=models.CASCADE, 
        related_name='salary_increase_requests'
    )
    
    requested_salary = models.DecimalField(max_digits=10, decimal_places=2)
    
    reason = models.TextField(blank=True, null=True)
    
    status = models.CharField(
        max_length=20, 
        choices=RequestStatusChoices.choices,
        default=RequestStatusChoices.PENDING
    )

    class Meta:
        verbose_name = "Salary Increase Request"
        verbose_name_plural = "Salary Increase Requests"
        app_label = 'hr'

    @property
    def current_salary(self):
        if self.employee.position:
            return self.employee.position.base_salary
        return 0
    
    def __str__(self):
        emp_name = f"{self.employee.first_name} {self.employee.last_name}"
        return f"Salary Increase Request: {emp_name} (Current: {self.current_salary}, Requested: {self.requested_salary})"
