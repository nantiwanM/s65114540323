from django.contrib import admin
from accounts.models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'formatted_date_joined')

    def formatted_date_joined(self, obj):
        return obj.date_joined.strftime('%d/%m/%Y %H:%M')  # กำหนดรูปแบบวันที่
    formatted_date_joined.short_description = 'วันที่สมัคร'

admin.site.register(UserProfile, UserProfileAdmin)