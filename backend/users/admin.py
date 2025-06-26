from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, UserProfile, UserSession, PasswordResetToken


class UserProfileInline(admin.StackedInline):
    """Inline admin for UserProfile"""
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('bio', 'specialization', 'license_number', 'years_of_experience', 
              'emergency_contact', 'emergency_contact_name', 'notification_preferences', 
              'privacy_settings')


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin interface for User model"""
    
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'full_name', 'role', 'is_verified', 'is_active', 'date_joined')
    list_filter = ('role', 'is_verified', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 
                                     'date_of_birth', 'address', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 
                                   'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('AlzCarePlus', {'fields': ('role', 'is_verified')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )
    
    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'Full Name'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin interface for UserProfile model"""
    
    list_display = ('user', 'specialization', 'years_of_experience', 'emergency_contact')
    list_filter = ('years_of_experience', 'created_at')
    search_fields = ('user__username', 'user__email', 'specialization')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Professional Info', {'fields': ('bio', 'specialization', 'license_number', 
                                         'years_of_experience')}),
        ('Emergency Contact', {'fields': ('emergency_contact', 'emergency_contact_name')}),
        ('Preferences', {'fields': ('notification_preferences', 'privacy_settings')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    """Admin interface for UserSession model"""
    
    list_display = ('user', 'ip_address', 'login_time', 'logout_time', 'is_active')
    list_filter = ('is_active', 'login_time', 'logout_time')
    search_fields = ('user__username', 'user__email', 'ip_address')
    readonly_fields = ('session_key', 'ip_address', 'user_agent', 'login_time', 'logout_time')
    
    fieldsets = (
        ('Session Info', {'fields': ('user', 'session_key', 'is_active')}),
        ('Connection Info', {'fields': ('ip_address', 'user_agent')}),
        ('Timestamps', {'fields': ('login_time', 'logout_time')}),
    )
    
    def has_add_permission(self, request):
        return False  # Sessions are created automatically


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    """Admin interface for PasswordResetToken model"""
    
    list_display = ('user', 'token_preview', 'created_at', 'expires_at', 'is_used', 'is_expired')
    list_filter = ('is_used', 'created_at', 'expires_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('token', 'created_at', 'expires_at')
    
    fieldsets = (
        ('Token Info', {'fields': ('user', 'token', 'is_used')}),
        ('Timestamps', {'fields': ('created_at', 'expires_at')}),
    )
    
    def token_preview(self, obj):
        """Show first 8 characters of token"""
        return f"{obj.token[:8]}..." if obj.token else ""
    token_preview.short_description = 'Token Preview'
    
    def is_expired(self, obj):
        """Check if token is expired"""
        return obj.is_expired()
    is_expired.boolean = True
    is_expired.short_description = 'Expired'
    
    def has_add_permission(self, request):
        return False  # Tokens are created automatically 