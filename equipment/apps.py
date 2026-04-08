from django.apps import AppConfig


class EquipmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'equipment'
    def ready(self):
        from .signals import connect_hr_signals
        connect_hr_signals()
