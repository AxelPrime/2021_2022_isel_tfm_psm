from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from ..models import CustomUser
from ..forms import CustomUserCreationForm, CustomUserChangeForm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('groups', 'user_permissions', 'is_superuser', 'is_staff', 'is_active')}),
        ('Login Info', {'fields': ('date_joined', 'last_login')}),
        ('User Type', {'fields': ('user_type', 'professional_certificate', 'care_house')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'first_name',
                'last_name',
                'user_type',
                'professional_certificate',
                'care_house',
                'is_superuser',
                'is_staff',
                'is_active'
            )
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
