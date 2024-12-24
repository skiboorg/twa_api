from django.contrib import admin
from .models import *
class FileInline(admin.TabularInline):
    model = File
    extra = 0

class LinkInline(admin.TabularInline):
    model = Link
    extra = 0

class UserTaskFileInline(admin.TabularInline):
    model = UserTaskFile
    extra = 0

class UserTaskLinkInline(admin.TabularInline):
    model = UserTaskLink
    extra = 0


class TaskAdmin(admin.ModelAdmin):
    model = Task
    search_fields = ('id','name')
    list_filter = (
        'in_work', 'in_review', 'is_done'
    )
    list_display = (
        'id',
        'name',
                    'short_description',
                    'price','in_work','in_review','is_done','deadline_date',)
    inlines = [FileInline,LinkInline]

class UserTaskAdmin(admin.ModelAdmin):
    model = UserTask
    search_fields = ('task__id','task__name','user__tg_id','user__username')
    list_filter = (
        'need_verify',
    )
    list_display = ('user','task__id','task__name','created_at','need_verify'
                    )
    inlines = [UserTaskFileInline,UserTaskLinkInline]


admin.site.register(Task,TaskAdmin)
admin.site.register(Filter)
admin.site.register(Level)
admin.site.register(UserTask,UserTaskAdmin)