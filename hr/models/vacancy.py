 
from django.db import models
from core.models import BaseModel


class Vacancy(BaseModel):
    position = models.ForeignKey('JobPosition', on_delete=models.CASCADE, related_name='vacancies')
    number_of_positions = models.PositiveIntegerField(default=1)
    description = models.TextField(blank=True, null=True)
    required_qualifications = models.TextField(blank=True, null=True)
    responsibilities = models.TextField(blank=True, null=True)
    is_open = models.BooleanField(default=True)
    close_date = models.DateField(null=True, blank=True)
    open_date = models.DateField(auto_now_add=False , auto_now=False , null=True , blank=True)
    class Meta:
        verbose_name = 'Vacancy'
        verbose_name_plural = 'Vacancies'
        app_label = 'hr'
    def __str__(self):
        return f"Vacancy for {self.position.title}"
    
