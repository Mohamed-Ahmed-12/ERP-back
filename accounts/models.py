from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models import BaseModel
from sites.models import Site

class User(AbstractUser):
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')