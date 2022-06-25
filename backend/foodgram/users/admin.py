from django.contrib import admin

from users import models


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'password', 'email')
    list_filter = ('username', 'email')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'following')


admin.site.register(models.User, UserAdmin)
