from django.apps import apps

def get_employee_model():
    if apps.is_installed("hr"):
        return apps.get_model("hr", "Employee")

    return apps.get_model("equipment", "EquipmentEmployee")

