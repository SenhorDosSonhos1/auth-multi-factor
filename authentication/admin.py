from django.contrib import admin
from authentication.models import CustomUser, Token
from django.contrib.auth.admin import UserAdmin

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Token)