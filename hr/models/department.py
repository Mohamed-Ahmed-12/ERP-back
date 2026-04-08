 
from django.db import models
from core.models import BaseModel

class Department(BaseModel):
    name = models.CharField(max_length=255 , unique=True)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
        app_label = 'hr'
    
    def __str__(self):
        return self.name
    
