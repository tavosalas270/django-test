from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterUserSerializer, UpdateUserSerializer, DeleteUserSerializer, LoginSerializer, PasswordResetSerializer
from .models import CustomUser
from drf_yasg.utils import swagger_auto_schema
from .api_responses import register_user_responses, update_user_responses, update_user_params, get_user_responses, login_user_responses

# Create your views here.
class RegisterUserView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(request_body=RegisterUserSerializer, responses=register_user_responses)
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Usuario creado con éxito'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateGetAllUserView(APIView):
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return CustomUser.objects.filter(status=True)
    
    @swagger_auto_schema(request_body=RegisterUserSerializer, responses=register_user_responses)
    def post(self, request):
        if not request.user.is_superuser:
            return Response({'message': 'No tienes permisos para realizar esta acción.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Usuario creado con éxito'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(responses=get_user_responses)
    def get(self, request):
        if not request.user.is_superuser:
            return Response({'message': 'No tienes permisos para realizar esta acción.'}, status=status.HTTP_403_FORBIDDEN)
        users = self.get_queryset()
        serializer = RegisterUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
            
class UpdateGetDeleteUserView(APIView):
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return CustomUser.objects.filter(status=True)
    
    @swagger_auto_schema(responses=get_user_responses, manual_parameters=update_user_params)
    def get(self, request, id=None):
        if not request.user.is_superuser:
            return Response({'message': 'No tienes permisos para realizar esta acción.'}, status=status.HTTP_403_FORBIDDEN)
        try:
            user = self.get_queryset().get(id=id)
            serializer = RegisterUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"message": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=UpdateUserSerializer, responses=update_user_responses, manual_parameters=update_user_params)
    def patch(self, request, id=None):
        if not request.user.is_superuser:
            return Response({'message': 'No tienes permisos para realizar esta acción.'}, status=status.HTTP_403_FORBIDDEN)
        try:
            user = self.get_queryset().get(id=id)
            serializer = UpdateUserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Usuario actualizado con éxito"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({"message": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    
    @swagger_auto_schema(request_body=DeleteUserSerializer, responses=update_user_responses, manual_parameters=update_user_params)
    def delete(self, request, id=None):
        if not request.user.is_superuser:
            return Response({'message': 'No tienes permisos para realizar esta acción.'}, status=status.HTTP_403_FORBIDDEN)
        try:
            user = self.get_queryset().get(id=id)
            user.status = False
            user.save()
            return Response({"message": "Usuario eliminado con éxito"}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"message": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=LoginSerializer, responses=login_user_responses)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, status=status.HTTP_200_OK)
    
class PasswordResetEmailView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=PasswordResetSerializer, responses={200: 'Correo enviado'})
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = CustomUser.objects.get(email=email)

            send_mail(
                'Recuperación de Contraseña',
                f'Hola {user.full_name}, haz clic en el siguiente enlace para recuperar tu contraseña: http://example.com/reset/{user.id}/',
                'noreply@example.com',
                [email],
                fail_silently=False,
            )

            return Response({'message': 'Correo de recuperación enviado'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)