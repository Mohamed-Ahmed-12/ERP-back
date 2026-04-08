from django.urls import path
from .views import installed_modules
urlpatterns = [
    path('modules/installed' ,installed_modules )
]