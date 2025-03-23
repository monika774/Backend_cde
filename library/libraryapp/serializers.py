from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Book

User = get_user_model()

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']
        read_only_fields = ['id', 'email']


class BookSerializer(serializers.ModelSerializer):
    added_by = AdminSerializer(read_only=True)  

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'isbn', 'publication_year', 
            'uuid_book', 'description', 'added_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'added_by']

    def create(self, validated_data):
        """ Only admins can create a book. """
        user = self.context['request'].user  
        if not user.is_staff:  
            raise serializers.ValidationError("Only admins can add books.")
        
        validated_data['added_by'] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """  Only admins can update a book. """
        user = self.context['request'].user
        if not user.is_staff:
            raise serializers.ValidationError("Only admins can update books.")

        return super().update(instance, validated_data)

    def delete(self, instance):
        """  Only admins can delete a book. """
        user = self.context['request'].user
        if not user.is_staff:
            raise serializers.ValidationError("Only admins can delete books.")

        instance.delete()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Creating token for normal user and admin user"""
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        
        token['username'] = user.username  
        token['email'] = user.email  
        token['is_admin'] = user.is_staff  

        return token



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['email', 'name', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )

        refresh = RefreshToken.for_user(user)
        return {
            'user': AdminSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'is_admin': user.is_staff
        }
