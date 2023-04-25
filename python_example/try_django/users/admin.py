from django.contrib import admin
from .models import Users

# Register your models here.
admin.site.register(Users)
"""
@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)
    search_fields = ('username',)
    filter_horizontal = ('groups', 'user_permissions')
    # readonly_fields = ('resign_time', 'pwdChangedTime')
"""