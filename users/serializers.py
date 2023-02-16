from datetime import timedelta

from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import User, StudyGroup, ResetPasswordToken


class StudyGroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyGroup
        fields = ['study_group']


class DefaultUserSerializer(serializers.ModelSerializer):
    study_group = serializers.CharField(max_length=20, allow_null=True)
    staff_for = serializers.PrimaryKeyRelatedField(many=True, required=False, read_only=True)

    def __init__(self, *args, exclude_staff=False, **kwargs):
        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)
        if exclude_staff:
            self.fields.pop('staff_for')

    def create(self, validated_data):
        password = validated_data['password']
        del validated_data['password']
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.avatar_url = validated_data.get('avatar_url', instance.avatar_url)
        instance.username = validated_data.get('username', instance.username)
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'study_group', 'id', 'staff_for', 'password',
                  'email', 'avatar_url', 'thumbnail', 'cats_account']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['thumbnail']


class TokenValidationMixin:
    def validate(self, attrs):
        token = attrs.get('token')
        expiry_time = getattr(settings, "TOKEN_EXPIRY_TIME", 24)
        try:
            reset_token = get_object_or_404(ResetPasswordToken, key=token)
        except (TypeError, ValueError, ValidationError,
                Http404, ResetPasswordToken.DoesNotExist):
            raise Http404("Bad password provided")

        if timezone.now() > reset_token.created_at + timedelta(hours=expiry_time):
            reset_token.delete()
            raise Http404("Token has been expired")
        return attrs


class TokenValidationSerializer(serializers.Serializer, TokenValidationMixin):
    token = serializers.CharField()


class PasswordTokenSerializer(serializers.Serializer, TokenValidationMixin):
    password = serializers.CharField(label="Password", style={'input_type': 'password'})
    token = serializers.CharField(allow_blank=True, allow_null=True)


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
