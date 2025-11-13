from django.contrib import admin

from core.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "name", "cpf", "state", "city", "img")
    search_fields = ["username", "name", "cpf"]
    exclude = ['first_name', 'last_name']

admin.site.register(User, UserAdmin)