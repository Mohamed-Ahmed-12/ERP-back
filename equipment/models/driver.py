from django.db import models
from core.models import BaseModel


class EquipmentEmployee(BaseModel):
    """
    Lightweight employee registry local to the Equipment module.

    Two sources:
        - 'hr'    : synced automatically from hr.Employee via signals
        - 'local' : manually entered when HR module is not installed
    """

    class Source(models.TextChoices):
        HR    = "hr",    "From HR Module"
        LOCAL = "local", "Local Entry"

    first_name   = models.CharField(max_length=255)
    last_name    = models.CharField(max_length=255)
    national_id  = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=50,  blank=True, null=True)

    # Soft reference to hr.Employee — null if HR not installed
    employee_id = models.UUIDField(null=True, blank=True, unique=True)
    source      = models.CharField(
        max_length=10,
        choices=Source.choices,
        default=Source.LOCAL,
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name

    class Meta:
        app_label = "equipment"
        db_table  = "equipment_employee"