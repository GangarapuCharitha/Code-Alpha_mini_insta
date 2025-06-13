from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')  # Columns to show in admin list view

admin.site.register(UserProfile, UserProfileAdmin)
