from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *

import requests





# class UserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'type', 'receiver_name', 'receiver_phone', 'amount', 'order_id', 'status', 'created_at')
#     search_fields = ['id', 'order_id']
#     list_filter = ('status', 'type')



# admin.site.register(NewUser, UserAdmin)

# admin.site.register(Media)


admin.site.register(NewUser)


admin.site.register(PermissionCategory)
admin.site.register(PermissionName)


admin.site.register(APILog)
