from django.db import models
from colorfield.fields import ColorField
from django_ckeditor_5.fields import CKEditor5Field

class Filter(models.Model):
    name = models.CharField(max_length=100)
    bg_color = ColorField(default='#FF0000')
    text_color = ColorField(default='#000000')

    def __str__(self):
        return self.name

class Level(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Task(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    filters = models.ManyToManyField(Filter)
    level = models.ForeignKey(Level, on_delete=models.CASCADE,blank=True, null=True)
    short_description = models.TextField(blank=True, null=True, default=None)
    full_description = CKEditor5Field( blank=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    deadline_date = models.DateField(blank=True, null=True)
    price = models.IntegerField(default=0, blank=True, null=True)

    is_done = models.BooleanField(default=False, null=False)
    in_work = models.BooleanField(default=False, null=False)
    in_review = models.BooleanField(default=False, null=False)

    done_date = models.DateField(blank=True, null=True)


    def __str__(self):
        return f'{self.created_at} | {self.name} '

    class Meta:
        ordering = ('-id',)

class File(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='tasks/', blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

class Link(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='links')
    url = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

class UserTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, blank=True, null=True, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    need_verify = models.BooleanField('Нужна проверка',default=False, null=False)
    need_extra_work = models.BooleanField('На доработке', default=False, null=False)
    decline = models.BooleanField('Отказался', default=False, null=False)
    timeout = models.BooleanField('Просрочено', default=False, null=False)
    worker_comment = models.TextField(blank=True, null=True, default=None)
    admin_comment = models.TextField(blank=True, null=True, default=None)


class UserTaskFile(models.Model):
    task = models.ForeignKey(UserTask, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='tasks/', blank=True, null=True)


class UserTaskLink(models.Model):
    task = models.ForeignKey(UserTask, on_delete=models.CASCADE, related_name='links')
    url = models.CharField(max_length=255, blank=True, null=True)


class RejectHistory(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)