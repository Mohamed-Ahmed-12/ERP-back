from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core.mixins import ApiResponseMixin 
from .serializers import UserProfileSerializer
from core.views import BaseAPIView

# Create your views here.
class UserProfile(BaseAPIView):
    permission_classes = [IsAuthenticated,]
    
    def get(self,request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(data=serializer.data)
    


class CustomTokenObtainPairView(ApiResponseMixin, TokenObtainPairView):
    custom_message = "Login successful. Welcome back."

class CustomTokenRefreshView(ApiResponseMixin, TokenRefreshView):
    custom_message = "Token refreshed successfully."