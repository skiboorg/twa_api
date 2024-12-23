import json
import random
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import *
from rest_framework import generics, viewsets, parsers

from django.conf import settings

import logging
logger = logging.getLogger(__name__)



class GetUser(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class UpdateUser(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer


    def get_object(self):
        return User.objects.get(uuid=self.request.user.uuid)


class CreatePassword(APIView):
    def post(self, request):
        data = request.data
        user = User.objects.get(tg_id=data.get('tg_id'))
        user.set_password(data.get('password'))
        user.save()
        return Response(status=status.HTTP_200_OK)


class CheckUser(APIView):
    def post(self, request):
        data = request.data
        user, created = User.objects.get_or_create(tg_id=data.get('id'))
        if created:
            user.firstname = data.get('first_name')
            user.lastname = data.get('last_name')
            user.username = data.get('username')
            user.photo_url = data.get('photo_url')
            user.save()
            return Response({"status": "created", "tg_id":user.tg_id}, status=200)
        else:
            return Response({"status": "exists", "tg_id":user.tg_id}, status=200)