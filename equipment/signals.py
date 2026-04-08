from django.apps import apps
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

def connect_hr_signals():
    if not apps.is_installed("hr"):
        return

    Employee = apps.get_model("hr", "Employee")
    EquipmentEmployee = apps.get_model("equipment", "EquipmentEmployee")

    @receiver(post_save, sender=Employee, dispatch_uid="sync_employee_to_equipment_employee")
    def sync_employee_to_equipment_employee(sender, instance, created, **kwargs):
        EquipmentEmployee.objects.update_or_create(
            employee_id=instance.guid,
            defaults={
                "first_name": instance.first_name,
                "last_name": instance.last_name,
                "national_id": instance.national_id,
                "phone_number": instance.phone_number,
                "source": EquipmentEmployee.Source.HR,
            },
        )

    @receiver(post_delete, sender=Employee, dispatch_uid="delete_equipment_employee_on_employee_delete")
    def delete_equipment_employee_on_employee_delete(sender, instance, **kwargs):
        EquipmentEmployee.objects.filter(employee_id=instance.guid).delete()