from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import *

class UserServiceInline(admin.TabularInline):  # Можно заменить на StackedInline для другого вида
    model = UserService
    extra = 1  # Количество пустых форм для добавления новых записей
    verbose_name = "User Service"
    verbose_name_plural = "User Services"
    fk_name = "user"  # Указывает, какой ForeignKey связывает UserService с User


class UserAdmin(BaseUserAdmin):
    list_display = (
        'firstname',
        'lastname',
        'date_joined',


    )
    ordering = ('id',)
    inlines = [UserServiceInline]
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
admin.site.register(SocialService)





