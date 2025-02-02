from django.urls import path,include
from . import views

urlpatterns = [
    path('me', views.GetUser.as_view()),
    path('update', views.UpdateUser.as_view()),
    path('check_user', views.CheckUser.as_view()),
    path('social_services', views.GetSocialServices.as_view()),
    path('social_action', views.SocialAction.as_view()),
    path('create_password', views.CreatePassword.as_view()),
    path('new_request', views.NewRequest.as_view()),

]
