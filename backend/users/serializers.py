from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User, UserProfile, PasswordResetToken
import uuid
from datetime import timedelta
from django.utils import timezone


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)
    profile_picture = serializers.ImageField(required=False)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 'password', 
            'confirm_password', 'phone_number', 'date_of_birth', 'address',
            'role', 'profile_picture'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True},
        }
    
    def validate(self, attrs):
        """Validate registration data"""
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords don't match")
        
        # Validate password strength
        try:
            validate_password(attrs['password'])
        except ValidationError as e:
            raise serializers.ValidationError({'password': e.messages})
        
        # Check if username already exists
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({'username': 'Username already exists'})
        
        # Check if email already exists
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({'email': 'Email already exists'})
        
        return attrs
    
    def create(self, validated_data):
        """Create new user"""
        validated_data.pop('confirm_password')
        profile_picture = validated_data.pop('profile_picture', None)
        
        user = User.objects.create_user(**validated_data)
        
        # Create user profile
        UserProfile.objects.create(user=user)
        
        # Handle profile picture
        if profile_picture:
            user.profile_picture = profile_picture
            user.save()
        
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        """Validate login credentials"""
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include username and password')
        
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile"""
    
    user = serializers.SerializerMethodField()
    profile_picture_url = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'bio', 'specialization', 'license_number',
            'years_of_experience', 'emergency_contact', 'emergency_contact_name',
            'notification_preferences', 'privacy_settings', 'profile_picture_url',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_user(self, obj):
        """Get user information"""
        user = obj.user
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'full_name': user.full_name,
            'phone_number': user.phone_number,
            'date_of_birth': user.date_of_birth,
            'address': user.address,
            'role': user.role,
            'role_display': user.get_role_display(),
            'is_verified': user.is_verified,
            'is_active': user.is_active,
            'date_joined': user.date_joined,
        }
    
    def get_profile_picture_url(self, obj):
        """Get profile picture URL"""
        if obj.user.profile_picture:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.user.profile_picture.url)
            return obj.user.profile_picture.url
        return None


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user information"""
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'phone_number',
            'date_of_birth', 'address', 'profile_picture'
        ]
    
    def validate_email(self, value):
        """Validate email uniqueness"""
        user = self.context['request'].user
        if User.objects.exclude(id=user.id).filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value


class PasswordChangeSerializer(serializers.Serializer):
    """Serializer for password change"""
    
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_new_password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        """Validate password change data"""
        if attrs['new_password'] != attrs['confirm_new_password']:
            raise serializers.ValidationError("New passwords don't match")
        
        # Validate new password strength
        try:
            validate_password(attrs['new_password'])
        except ValidationError as e:
            raise serializers.ValidationError({'new_password': e.messages})
        
        return attrs
    
    def validate_old_password(self, value):
        """Validate old password"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is incorrect')
        return value


class PasswordResetRequestSerializer(serializers.Serializer):
    """Serializer for password reset request"""
    
    email = serializers.EmailField()
    
    def validate_email(self, value):
        """Validate email exists"""
        if not User.objects.filter(email=value, is_active=True).exists():
            raise serializers.ValidationError('No active user found with this email')
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Serializer for password reset confirmation"""
    
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_new_password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        """Validate password reset data"""
        if attrs['new_password'] != attrs['confirm_new_password']:
            raise serializers.ValidationError("Passwords don't match")
        
        # Validate new password strength
        try:
            validate_password(attrs['new_password'])
        except ValidationError as e:
            raise serializers.ValidationError({'new_password': e.messages})
        
        # Validate token
        try:
            reset_token = PasswordResetToken.objects.get(
                token=attrs['token'],
                is_used=False
            )
            if reset_token.is_expired():
                raise serializers.ValidationError({'token': 'Token has expired'})
            attrs['reset_token'] = reset_token
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError({'token': 'Invalid or expired token'})
        
        return attrs


class UserListSerializer(serializers.ModelSerializer):
    """Serializer for listing users"""
    
    full_name = serializers.CharField(source='full_name', read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    profile_picture_url = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'role', 'role_display', 'phone_number', 'is_verified', 'is_active',
            'profile_picture_url', 'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']
    
    def get_profile_picture_url(self, obj):
        """Get profile picture URL"""
        if obj.profile_picture:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.profile_picture.url)
            return obj.profile_picture.url
        return None 