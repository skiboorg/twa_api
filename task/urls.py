from django.urls import path,include
from . import views


urlpatterns = [
    path('filters', views.GetFilters.as_view()),
    path('tasks', views.GetTasks.as_view()),
    path('task/<pk>', views.GetTask.as_view()),
]
