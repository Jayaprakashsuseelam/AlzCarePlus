from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'users'

urlpatterns = [
    # Authentication endpoints
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User profile and details
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('me/', views.UserDetailView.as_view(), name='user_detail'),
    path('info/', views.user_info_view, name='user_info'),
    
    # Password management
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('reset-password/', views.PasswordResetRequestView.as_view(), name='reset_password_request'),
    path('reset-password/confirm/', views.PasswordResetConfirmView.as_view(), name='reset_password_confirm'),
    
    # Admin endpoints (optional)
    path('list/', views.UserListView.as_view(), name='user_list'),
    path('current/', views.current_user_view, name='current_user'),
    path('verify/<int:user_id>/', views.verify_user_view, name='verify_user'),
    path('stats/', views.user_stats_view, name='user_stats'),
] 