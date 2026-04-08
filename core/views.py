from django.apps import apps
from rest_framework.decorators import api_view
from rest_framework.response import Response

TRACKED_MODULES = [
    "hr",
    "merchant",
    "warehouse",
    "finance",
    "payroll",
    'equipment'
]

@api_view(["GET"])
def installed_modules(request):
    return Response({
        module: apps.is_installed(module)
        for module in TRACKED_MODULES
    })