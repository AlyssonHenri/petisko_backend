from django.contrib import admin

from core.models import User, Match

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "name", "cpf", "state", "city", "img")
    search_fields = ["username", "name", "cpf"]
    exclude = ['first_name', 'last_name']

class MatchAdmin(admin.ModelAdmin):
    list_display = ("id", "petPrincipal", "petMatch")
    search_fields = ["petPrincipal__name", "petMatch__name"]

admin.site.register(User, UserAdmin)
admin.site.register(Match, MatchAdmin)
