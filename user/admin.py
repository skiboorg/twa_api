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
        'username',
        'firstname',
        'lastname',
        'balance',
        'rating',


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
    search_fields = ('id','wallet',)

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
         'wallet',
             'rating',
             'is_verified'


         )}
         ),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups',)}),)

class WithdrawalRequestAdmin(admin.ModelAdmin):
    model = WithdrawalRequest
    search_fields = ('user__tg_id','user__username')
    list_filter = (
        'is_done',
    )
    list_display = ('user','amount','created_at','is_done')

admin.site.register(User,UserAdmin)
admin.site.register(SocialService)
admin.site.register(WithdrawalRequest, WithdrawalRequestAdmin)





