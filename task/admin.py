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
    inlines = [FileInline,LinkInline]

class UserTaskAdmin(admin.ModelAdmin):
    model = UserTask
    inlines = [UserTaskFileInline,UserTaskLinkInline]


admin.site.register(Task,TaskAdmin)
admin.site.register(Filter)
admin.site.register(Level)
admin.site.register(UserTask,UserTaskAdmin)