from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import DBUser

UserAdmin.fieldsets += (
    ('Extra Fields', {'fields': ('bio', 'role',)}),
)

admin.site.register(DBUser, UserAdmin)
