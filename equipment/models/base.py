from django.db import models
from django.apps import apps

from core.models import BaseModel
from core.mixins import OptionalFKMixin


class EquipmentType(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    drivable = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "equipment_type"
        app_label = 'equipment'
    


class EquipmentBrand(BaseModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "equipment_brand"
        app_label = 'equipment'


class WorkType(BaseModel):
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    # M2M with EquipmentType (equipment_type_work_types)
    equipment_types = models.ManyToManyField(
        'EquipmentType',
        related_name="work_types",
        blank=True,
        db_table="equipment_type_work_types",
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "work_type"
        app_label = 'equipment'


class Equipment(BaseModel):
    class Status(models.TextChoices):
        ACTIVE            = "active",            "Active"
        INACTIVE          = "inactive",          "Inactive"
        UNDER_MAINTENANCE = "under_maintenance", "Under Maintenance"
        RETIRED           = "retired",           "Retired"

    serial_number = models.CharField(max_length=255, unique=True)
    name          = models.CharField(max_length=255)
    model         = models.CharField(max_length=255, blank=True, null=True)
    status        = models.CharField(
        max_length=50,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    equipment_type = models.ForeignKey(
        'EquipmentType',
        on_delete=models.PROTECT,
        related_name="equipments",
    )
    equipment_brand = models.ForeignKey(
        'EquipmentBrand',
        on_delete=models.PROTECT,
        related_name="equipments",
    )

    main_driver = models.ForeignKey(
        'equipment.EquipmentEmployee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="main_driver_equipments",
    )
    sub_driver = models.ForeignKey(
        'equipment.EquipmentEmployee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sub_driver_equipments",
    )

    def __str__(self):
        return f"{self.name} ({self.serial_number})"

    class Meta:
        app_label = "equipment"
        db_table  = "equipment"


# class Consumable(models.Model):
#     class Status(models.TextChoices):
#         AVAILABLE = "AVAILABLE", "Available"
#         IN_USE = "IN_USE", "In Use"
#         DEPLETED = "DEPLETED", "Depleted"
#         RESOLVED = "RESOLVED", "Resolved"

#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     quantity = models.IntegerField(default=0)
#     status = models.CharField(max_length=50, choices=Status.choices, default=Status.AVAILABLE)

#     # FK to ItemType (Warehouse module)
#     item_type = models.ForeignKey(
#         "warehouse.ItemType",
#         on_delete=models.PROTECT,
#         related_name="consumables",
#     )
#     equipment = models.ForeignKey(
#         Equipment,
#         on_delete=models.CASCADE,
#         related_name="consumables",
#     )

#     def __str__(self):
#         return f"Consumable [{self.item_type}] for {self.equipment}"

#     class Meta:
#         db_table = "consumable"


# class ConsumableResolution(models.Model):
#     class ResolutionType(models.TextChoices):
#         DISPOSED = "DISPOSED", "Disposed"
#         RETURNED = "RETURNED", "Returned"
#         TRANSFERRED = "TRANSFERRED", "Transferred"

#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     resolution_type = models.CharField(max_length=50, choices=ResolutionType.choices)
#     consumable = models.ForeignKey(
#         Consumable,
#         on_delete=models.CASCADE,
#         related_name="resolutions",
#     )

#     def __str__(self):
#         return f"{self.resolution_type} — {self.consumable}"

#     class Meta:
#         db_table = "consumable_resolution"


# class SarkyLog(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     worked_hours = models.FloatField()
#     date = models.DateField()

#     equipment = models.ForeignKey(
#         Equipment,
#         on_delete=models.CASCADE,
#         related_name="sarky_logs",
#     )
#     work_type = models.ForeignKey(
#         WorkType,
#         on_delete=models.PROTECT,
#         related_name="sarky_logs",
#     )
#     driver = models.ForeignKey(
#         "hr.Employee",
#         on_delete=models.PROTECT,
#         related_name="sarky_logs",
#     )

#     def __str__(self):
#         return f"SarkyLog {self.date} — {self.equipment} ({self.worked_hours}h)"

#     class Meta:
#         db_table = "sarky_log"


# class Document(models.Model):
#     class EntityType(models.TextChoices):
#         EQUIPMENT = "EQUIPMENT", "Equipment"
#         EMPLOYEE = "EMPLOYEE", "Employee"
#         MAINTENANCE = "MAINTENANCE", "Maintenance"
#         OTHER = "OTHER", "Other"

#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     entity_type = models.CharField(max_length=50, choices=EntityType.choices)
#     entity_id = models.UUIDField()  # Generic FK — points to any entity
#     name = models.CharField(max_length=255)

#     uploaded_by = models.ForeignKey(
#         "users.User",
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name="uploaded_documents",
#     )

#     def __str__(self):
#         return f"{self.name} ({self.entity_type}:{self.entity_id})"

#     class Meta:
#         db_table = "document"


# class MaintenanceType(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=255, unique=True)
#     active = models.BooleanField(default=True)

#     def __str__(self):
#         return self.name

#     class Meta:
#         db_table = "maintenance_type"


# class InSiteMaintenance(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     maintenance_date = models.DateTimeField()
#     status = models.CharField(max_length=100)

#     equipment = models.ForeignKey(
#         Equipment,
#         on_delete=models.CASCADE,
#         related_name="in_site_maintenances",
#     )
#     technician = models.ForeignKey(
#         "hr.Employee",
#         on_delete=models.PROTECT,
#         related_name="in_site_maintenances",
#     )
#     maintenance_type = models.ForeignKey(
#         MaintenanceType,
#         on_delete=models.PROTECT,
#         related_name="in_site_maintenances",
#     )

#     def __str__(self):
#         return f"Maintenance [{self.maintenance_type}] on {self.equipment} @ {self.maintenance_date}"

#     class Meta:
#         db_table = "in_site_maintenance"


# class MaintenanceConsumable(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     quantity = models.IntegerField()

#     maintenance = models.ForeignKey(
#         InSiteMaintenance,
#         on_delete=models.CASCADE,
#         related_name="maintenance_consumables",
#     )
#     item_type = models.ForeignKey(
#         "warehouse.ItemType",
#         on_delete=models.PROTECT,
#         related_name="maintenance_consumables",
#     )

#     def __str__(self):
#         return f"{self.quantity}x {self.item_type} for maintenance {self.maintenance_id}"

#     class Meta:
#         db_table = "maintenance_consumable"