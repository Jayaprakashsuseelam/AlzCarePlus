from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import models
from datetime import timedelta
import uuid
import logging

from .models import User, UserProfile, PasswordResetToken
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer,
    UserUpdateSerializer, PasswordChangeSerializer, PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer, UserListSerializer
)

logger = logging.getLogger(__name__)


class UserRegistrationView(APIView):
    """User registration endpoint"""
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Register a new user"""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Log the user in after registration
            login(request, user)
            
            # Get user profile data
            profile_serializer = UserProfileSerializer(user.profile, context={'request': request})
            
            return Response({
                'message': 'User registered successfully',
                'user': profile_serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """User login endpoint"""
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Login user"""
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            
            # Get user profile data
            profile_serializer = UserProfileSerializer(user.profile, context={'request': request})
            
            return Response({
                'message': 'Login successful',
                'user': profile_serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    """User logout endpoint"""
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Logout user"""
        logout(request)
        return Response({
            'message': 'Logout successful'
        }, status=status.HTTP_200_OK)


class UserProfileView(APIView):
    """User profile management"""
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get current user profile"""
        profile_serializer = UserProfileSerializer(request.user.profile, context={'request': request})
        return Response(profile_serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request):
        """Update user profile"""
        user_serializer = UserUpdateSerializer(request.user, data=request.data, partial=True, context={'request': request})
        profile_serializer = UserProfileSerializer(request.user.profile, data=request.data, partial=True, context={'request': request})
        
        if user_serializer.is_valid() and profile_serializer.is_valid():
            user_serializer.save()
            profile_serializer.save()
            
            # Return updated profile
            updated_profile = UserProfileSerializer(request.user.profile, context={'request': request})
            return Response({
                'message': 'Profile updated successfully',
                'user': updated_profile.data
            }, status=status.HTTP_200_OK)
        
        errors = {}
        if not user_serializer.is_valid():
            errors.update(user_serializer.errors)
        if not profile_serializer.is_valid():
            errors.update(profile_serializer.errors)
        
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeView(APIView):
    """Password change endpoint"""
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Change user password"""
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            return Response({
                'message': 'Password changed successfully'
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(APIView):
    """Password reset request endpoint"""
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Request password reset"""
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            
            # Generate reset token
            token = str(uuid.uuid4())
            expires_at = timezone.now() + timedelta(hours=24)
            
            # Create or update reset token
            PasswordResetToken.objects.filter(user=user, is_used=False).update(is_used=True)
            PasswordResetToken.objects.create(
                user=user,
                token=token,
                expires_at=expires_at
            )
            
            # TODO: Send email with reset link
            # For now, just return the token (in production, send via email)
            logger.info(f"Password reset token for {email}: {token}")
            
            return Response({
                'message': 'Password reset email sent successfully',
                'token': token  # Remove this in production
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    """Password reset confirmation endpoint"""
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Confirm password reset"""
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            reset_token = serializer.validated_data['reset_token']
            new_password = serializer.validated_data['new_password']
            
            # Update user password
            user = reset_token.user
            user.set_password(new_password)
            user.save()
            
            # Mark token as used
            reset_token.is_used = True
            reset_token.save()
            
            return Response({
                'message': 'Password reset successfully'
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListAPIView):
    """List all users (admin only)"""
    
    permission_classes = [IsAuthenticated]
    serializer_class = UserListSerializer
    queryset = User.objects.all().order_by('-date_joined')
    
    def get_queryset(self):
        """Filter users based on role and search"""
        queryset = User.objects.all().order_by('-date_joined')
        
        # Filter by role
        role = self.request.query_params.get('role', None)
        if role:
            queryset = queryset.filter(role=role)
        
        # Search by name or email
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                models.Q(first_name__icontains=search) |
                models.Q(last_name__icontains=search) |
                models.Q(email__icontains=search) |
                models.Q(username__icontains=search)
            )
        
        return queryset


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """User detail view (admin only)"""
    
    permission_classes = [IsAuthenticated]
    serializer_class = UserListSerializer
    queryset = User.objects.all()
    lookup_field = 'id'
    
    def destroy(self, request, *args, **kwargs):
        """Soft delete user"""
        user = self.get_object()
        user.is_active = False
        user.save()
        
        return Response({
            'message': 'User deactivated successfully'
        }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_view(request):
    """Get current user information"""
    profile_serializer = UserProfileSerializer(request.user.profile, context={'request': request})
    return Response(profile_serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_user_view(request, user_id):
    """Verify user account (admin only)"""
    user = get_object_or_404(User, id=user_id)
    user.is_verified = True
    user.save()
    
    return Response({
        'message': 'User verified successfully'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_stats_view(request):
    """Get user statistics (admin only)"""
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    verified_users = User.objects.filter(is_verified=True).count()
    
    # Users by role
    role_stats = {}
    for role, _ in User.ROLE_CHOICES:
        role_stats[role] = User.objects.filter(role=role).count()
    
    return Response({
        'total_users': total_users,
        'active_users': active_users,
        'verified_users': verified_users,
        'role_stats': role_stats
    }, status=status.HTTP_200_OK) 