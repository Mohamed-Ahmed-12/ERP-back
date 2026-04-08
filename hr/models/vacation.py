from django.db import models
from core.models import BaseModel

class VacationBalance(BaseModel):
    employee = models.OneToOneField(
        'Employee',
        on_delete=models.CASCADE, 
        related_name='vacation_balance'
    )
    
    total_days = models.PositiveIntegerField(default=0)
    used_days = models.PositiveIntegerField(default=0)

    @property
    def remaining_days(self):
        return self.total_days - self.used_days
    
    class Meta:
        verbose_name = 'Vacation Balance'
        verbose_name_plural = 'Vacation Balances'
        app_label = 'hr'
        
    def __str__(self):
        return f"Vacation Balance for {self.employee.first_name} {self.employee.last_name}: {self.remaining_days} days remaining"
 