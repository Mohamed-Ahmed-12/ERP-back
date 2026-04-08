 
from django.db import models
from core.models import BaseModel

class ContractTypeChoices(models.TextChoices):
    FULL_TIME = 'Full-time', 'Full-time'
    PART_TIME = 'Part-time', 'Part-time'
    CONTRACT = 'Contract', 'Contract'

class SeniorityLevel(models.TextChoices):
    ENTRY = "entry", "Entry"
    MID = "mid", "Mid"
    SENIOR = "senior", "Senior"
    DIRECTOR = "director", "Director"
    VP = "vp", "VP"
    C_SUITE = "c_suite", "C-Suite"
    
class JobPosition(BaseModel):
    """ like senior developer, hr manager, etc """
    contract_type = models.CharField(max_length=20, choices=ContractTypeChoices.choices)
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    title = models.CharField(max_length=255)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True, related_name='positions')
    seniority_level = models.CharField(
        max_length=20, choices=SeniorityLevel.choices, default=SeniorityLevel.MID , null=True , blank=True
    )
    class Meta:
        verbose_name = 'Job Position'
        verbose_name_plural = 'Job Positions'
        app_label = 'hr'
    def __str__(self):
        return self.title
