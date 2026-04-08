from django.urls import path
from dashboard.views import DashboardView
urlpatterns = [
    path('stats/' , DashboardView.as_view())
]