from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

    
from .serializers import UserProfileSerializer
# Create your views here.
class UserProfile(APIView):
    permission_classes = [IsAuthenticated,]
    
    def get(self,request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(data=serializer.data)