from equipment.views.base import EquipmentTypeViewSet , EquipmentViewSet , EquipmentEmployeeViewSet , EquipmentBrandViewSet
from rest_framework import routers

router = routers.DefaultRouter()

router.register('equipments' , EquipmentViewSet , 'equipments')
router.register('types' , EquipmentTypeViewSet , 'equipment-types')
router.register('brands' , EquipmentBrandViewSet , 'equipment-brands')
router.register('equipment-employee' , EquipmentEmployeeViewSet , 'equipment-employee')
urlpatterns = router.urls