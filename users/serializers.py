from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from .models import CustomUser

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_superuser = serializers.BooleanField(required=False)

    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'password', 'is_superuser']
    
    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Este campo es requerido", code="required")
        
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este usuario ya existe", code="duplicate")
        
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)  # Cifra la contraseña
        user.save()
        return user
    
class UpdateUserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'password']

    def validate_email(self, value):
        if value and CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este usuario ya existe", code="duplicate")
        return value
    
    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))
        return super().update(instance, validated_data)
    
class DeleteUserSerializer(serializers.ModelSerializer):
    status = serializers.BooleanField(required=True)

    class Meta:
        model = CustomUser
        fields = ['status']

    def update(self, instance, validated_data):
        if 'status' in validated_data:
            instance.status = validated_data['status']
        instance.save()
        return instance
    
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password']

    def validate(self, data):
        email = data.get('email', '')
        password = data.get('password', '')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Correo o contraseña incorrectos.")
        
        if not check_password(password, user.password):
            raise serializers.ValidationError("Correo o contraseña incorrectos.")

        if not user.status:
            raise serializers.ValidationError("El usuario no está activo.")

        data['user'] = user
        return data
    
class PasswordResetSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['email']

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Este campo es requerido", code="required")
        
        if not CustomUser.objects.filter(email=value, status=True).exists():
            raise serializers.ValidationError("No existe un usuario con este correo.", code="not_found")

        return value