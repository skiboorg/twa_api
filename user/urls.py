from django.urls import path,include
from . import views

urlpatterns = [
    path('me', views.GetUser.as_view()),
    path('update', views.UpdateUser.as_view()),
    path('check_user', views.CheckUser.as_view()),
    path('create_password', views.CreatePassword.as_view()),

]
