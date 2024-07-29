from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserChangeForm, CustomUserCreationForm

# Register your models here.


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        'username',
        'email',
        'age',
        'is_staff',
    ]
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'fields': (
                'age',
            ),
        }),
    )
    fieldsets = UserAdmin.fieldsets + (
        (None, {
            'fields': (
                'age',
            ),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
