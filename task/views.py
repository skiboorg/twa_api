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
    queryset = Task.objects.filter(is_done=False,in_work=False)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter

class GetTask(generics.RetrieveAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()


