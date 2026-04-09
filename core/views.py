from django.apps import apps
from rest_framework.decorators import api_view

from rest_framework.views import APIView
from rest_framework import viewsets
from core.response import success_response
from core.mixins import ApiResponseMixin


class BaseAPIView(ApiResponseMixin, APIView):
    pass

class BaseViewSet(ApiResponseMixin, viewsets.ModelViewSet):
    pass

# ========================
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
    return success_response({
        module: apps.is_installed(module)
        for module in TRACKED_MODULES
    })