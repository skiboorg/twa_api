from rest_framework import serializers
from .models import *
from datetime import date

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = '__all__'


class FilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filter
        fields = '__all__'


class TaskShortSerializer(serializers.ModelSerializer):
    filters = FilterSerializer(many=True, read_only=True)
    level = LevelSerializer(many=False, read_only=True)
    days_until_deadline = serializers.SerializerMethodField()
    class Meta:
        model = Task
        exclude = ['full_description']

    def get_days_until_deadline(self, obj):
        if obj.deadline_date:
            delta = obj.deadline_date - date.today()
            return delta.days
        return None

class TaskSerializer(serializers.ModelSerializer):
    filters = FilterSerializer(many=True, read_only=True)
    files = FileSerializer(many=True, read_only=True)
    links = LinkSerializer(many=True, read_only=True)
    level = LevelSerializer(many=False, read_only=True)
    days_until_deadline = serializers.SerializerMethodField()
    class Meta:
        model = Task
        fields = '__all__'
    def get_days_until_deadline(self, obj):
        if obj.deadline_date:
            delta = obj.deadline_date - date.today()
            return delta.days
        return None


class UserTaskFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTaskFile
        fields = '__all__'


class UserTaskLinkLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTaskLink
        fields = '__all__'


class UserTaskShortSerializer(serializers.ModelSerializer):
    task = TaskShortSerializer(many=False, read_only=True)
    class Meta:
        model = UserTask
        fields = '__all__'
