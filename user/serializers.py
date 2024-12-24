
from django.utils import timezone
from datetime import timedelta

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction

from rest_framework import exceptions, serializers, status, generics
from .models import *
from djoser.conf import settings
from task.serializers import UserTaskShortSerializer
import logging
logger = logging.getLogger(__name__)




class SocialServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialService
        fields = '__all__'


class UserSocialServiceSerializer(serializers.ModelSerializer):
    service = SocialServiceSerializer(many=False, read_only=True)
    class Meta:
        model = UserService
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    tasks = UserTaskShortSerializer(many=True,read_only=True)
    social = UserSocialServiceSerializer(many=True,read_only=True)
    class Meta:
        model = User
        fields = [
            'uuid',
            'photo_url',
            'firstname',
            'lastname',
            'username',
            'tasks',
            'balance',
            'rating',
            'is_verified',
            'wallet',
            'social'
        ]

        extra_kwargs = {
            'password': {'required': False},

        }


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    default_error_messages = {
        "cannot_create_user": settings.CONSTANTS.messages.CANNOT_CREATE_USER_ERROR
    }

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            'ton_wallet',
            'used_ref_code',
            'password',
        )

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get("password")


        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            print(e)
            raise serializers.ValidationError(
                {"password": serializer_error["non_field_errors"]}
            )

        return attrs

    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")

        return user

    def perform_create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            used_ref_code = validated_data.get("used_ref_code",None)
            print(used_ref_code)
            if not used_ref_code:
                user.used_ref_code = 'ET-000000'
            else:
                user_with_code = User.objects.filter(own_ref_code=used_ref_code).first()
                if not user_with_code:
                    user.used_ref_code = 'ET-000000'
            user.is_active = True
            user.own_ref_code = 'ET-' + create_random_string(False, 8)
            user.save(update_fields=["is_active",'used_ref_code','own_ref_code'])

        return user


