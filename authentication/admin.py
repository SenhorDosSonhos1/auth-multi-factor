from django.contrib import admin
from authentication.models import CustomUser
from django.contrib.auth.admin import UserAdmin

admin.site.register(CustomUser, UserAdmin)