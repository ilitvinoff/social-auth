from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import UserAccount


class UserAccountSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True, allow_null=False, allow_blank=False, validators=[
        UniqueValidator(queryset=UserAccount.objects.all(), message="Email field must be unique.")])

    class Meta:
        model = UserAccount
        fields = ('uuid', 'email', 'is_active')
        read_only_fields = ('is_active',)


class CreateUserAccountSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[
        UniqueValidator(queryset=UserAccount.objects.all(), message="Email field must be unique.")])
    password = serializers.CharField(min_length=8, required=True)

    def validate_password(self, password):
        validate_password(password, user=UserAccount(email=self.initial_data['email']))
        return password

    def create(self, validated_data):
        user = UserAccount.objects.create_user(validated_data['email'], validated_data['password'])
        return user

    class Meta:
        model = UserAccount
        fields = ('uuid', 'email', 'password')
