from django.contrib import admin
from users import models

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'password', 'email')

# TODO: Настроить админку

admin.site.register(models.User, UserAdmin)