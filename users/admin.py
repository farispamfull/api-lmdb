from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import MyUserChangeForm


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )


admin.site.register(User, MyUserAdmin)