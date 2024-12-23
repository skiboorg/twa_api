from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import *


class UserAdmin(BaseUserAdmin):
    list_display = (
        'firstname',
        'lastname',
        'date_joined',


    )
    ordering = ('id',)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'firstname',
                    'lastname',
                       'password1',
                       'password2',
                       ), }),)
    search_fields = ('id','ton_wallet',)

    fieldsets = (
        (None, {'fields': ()}),
        ('Personal info',
         {'fields': (

         'uuid',
         'photo_url',
         'firstname',
         'lastname',
         'username',
         'balance',
             'rating',
             'is_verified'


         )}
         ),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups',)}),)


admin.site.register(User,UserAdmin)





