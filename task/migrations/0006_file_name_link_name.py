# Generated by Django 5.1.4 on 2025-01-05 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0005_usertask_decline_usertask_need_extra_work_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='link',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]