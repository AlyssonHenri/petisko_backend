from django.contrib import admin

from core.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = (id, "username", "img")
    search_fields = [("username")]

admin.site.register(User, UserAdmin)