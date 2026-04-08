from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

        
class UserProfileSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups',]
