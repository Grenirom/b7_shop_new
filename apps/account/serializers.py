from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', )


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=20,
                                     required=True, write_only=True)
    password_confirm = serializers.CharField(min_length=8, max_length=20,
                                             required=True, write_only=True)

    class Meta:
        model = User
        fields = ('emails', 'password', 'password_confirm')

    def validate(self, attrs):
        password = attrs['password']
        password_confirm = attrs.pop('password_confirm')

        if password != password_confirm:
            raise serializers.ValidationError('Пароли не совпали!')
        validate_password(password)
        return attrs

    def create(self, validated_data):
        password = validated_data['password']
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LogOutSerialzer(serializers.Serializer):
    refresh = serializers.CharField(required=True, write_only=True)