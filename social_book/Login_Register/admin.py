from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UploadedFiles
# from .forms import RegistrationForm, UserUpdateForm

# Register your models here.
class CustomUserAdmin(UserAdmin):
    # add_form = RegistrationForm
    # form = UserUpdateForm
    model = CustomUser
    list_display = ("email", "is_staff", "is_active", 'full_name', 'public_visibility', 'date_of_birth', 'city', 'state', 'age', 'profile_image')
    list_filter = ("email", "is_staff", "is_active", 'public_visibility')
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ('Personal Info', {'fields': ('full_name', 'city', 'state', 'date_of_birth', 'profile_image')}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    readonly_fields = ('age',)
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}),
    )
    search_fields = ("email",)
    ordering = ("email",)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UploadedFiles)