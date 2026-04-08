from django.contrib import admin
from .models import Equipment , EquipmentType , EquipmentBrand
# Register your models here.
admin.site.register(EquipmentBrand)
admin.site.register(EquipmentType)
admin.site.register(Equipment)