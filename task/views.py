from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, viewsets
from rest_framework.views import APIView
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *
import django_filters
from rest_framework.parsers import MultiPartParser

class TaskFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')  # Фильтр по имени (независимо от регистра)
    filters = django_filters.ModelMultipleChoiceFilter(queryset=Filter.objects.all())  # Фильтр по связанной модели
    level = django_filters.ModelChoiceFilter(queryset=Level.objects.all())  # Фильтр по уровню
    deadline_date = django_filters.DateFilter()  # Точная дата
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr='gte')  # Минимальная цена
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr='lte')  # Максимальная цена

    class Meta:
        model = Task
        fields = ['name', 'filters', 'level', 'deadline_date', 'price_min', 'price_max']

class GetFilters(generics.ListAPIView):
    serializer_class = FilterSerializer
    queryset = Filter.objects.all()

class GetTasks(generics.ListAPIView):
    serializer_class = TaskShortSerializer
    queryset = Task.objects.filter(is_done=False,in_work=False,in_review=False)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter

class GetTask(generics.RetrieveAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()


class TakeVerify(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        comment = request.data.get('comment')
        id = request.data.get('id')
        files = request.FILES.getlist('files')
        links = request.data.getlist('links')
        print(comment, id, files, links)

        user_task = UserTask.objects.get(task_id=id)
        print(user_task)
        user_task.task.in_work=False
        user_task.task.in_review=True
        user_task.task.save()
        user_task.need_verify = True
        user_task.worker_comment = comment
        user_task.save()

        for file in files:
            UserTaskFile.objects.create(task=user_task, file=file)
        for link in links:
            UserTaskLink.objects.create(task=user_task, url=link)
        return Response(status=200)
class TakeTask(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        result = {'success':False}
        task_id = request.data.get('id', None)
        user = request.user
        if task_id is not None:
            task = Task.objects.get(id=task_id)
            UserTask.objects.create(
                user=user,
                task=task
            )
            task.in_work = True
            task.save()
            result = {'success': True, 'message': 'Задача принята'}
        return Response(result, status=200)