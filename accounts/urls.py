
from django.urls import path

from .views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
)
from .views import UserProfile

urlpatterns = [
    path('login/',CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('me/', UserProfile.as_view(), name='user_profile'),
]