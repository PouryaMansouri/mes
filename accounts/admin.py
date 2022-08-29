from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext as _
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """ User admin """
    add_form = UserCreationForm
    form = UserChangeForm

    list_display = ('id', 'email', 'first_name', 'last_name', 'is_staff')

    search_fields = ('email', 'first_name', 'last_name', 'phone_number')
    list_filter = ('is_staff',)
    ordering = ('-id',)
    readonly_fields = ('id', 'date_joined', 'last_login')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )