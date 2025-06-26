from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', views.UserRegistrationView.as_view(), name='register'),
    path('auth/login/', views.UserLoginView.as_view(), name='login'),
    path('auth/logout/', views.UserLogoutView.as_view(), name='logout'),
    
    # Profile management
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/change-password/', views.PasswordChangeView.as_view(), name='change-password'),
    
    # Password reset
    path('auth/password-reset/', views.PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('auth/password-reset/confirm/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    
    # User management (admin)
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:id>/', views.UserDetailView.as_view(), name='user-detail'),
    path('users/<int:user_id>/verify/', views.verify_user_view, name='verify-user'),
    path('users/stats/', views.user_stats_view, name='user-stats'),
    
    # Current user
    path('me/', views.current_user_view, name='current-user'),
] 