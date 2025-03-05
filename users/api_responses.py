from drf_yasg import openapi
from .serializers import RegisterUserSerializer

get_user_responses = {
    200: openapi.Response(
        description="Usuario/s encontrado/s",
        schema=RegisterUserSerializer(many=True)
    ),
}

register_user_responses = {
    201: openapi.Response(
        description="Usuario creado",
        examples={
            "application/json": {"message": "Usuario creado"}
        }
    ),
    400: openapi.Response(
        description="Error de validación",
        examples={
            "application/json": {
                "email": "El campo email es obligatorio.",
                "email": "Ya existe un usuario con este email"
            }
        }
    ),
}

login_user_responses = {
    200: openapi.Response(
        description="Sesion iniciada",
        examples={
            "application/json": {
                "access": "access_token_generado",
                "refresh": "refresh_token_generado"
            }
        }
    ),
    400: openapi.Response(
        description="Error de validación",
        examples={
            "application/json": {
                "email": "El campo email es obligatorio.",
                "password": "La contraseña es obligatoria.",
            }
        }
    ),
    401: openapi.Response(
        description="Credenciales inválidas",
        examples={
            "application/json": {
                "detail": "Correo o contraseña incorrectos."
            }
        }
    ),
    403: openapi.Response(
        description="Usuario no activo",
        examples={
            "application/json": {
                "detail": "El usuario no está activo."
            }
        }
    )
}

update_user_responses = {
    200: openapi.Response(
        description="Usuario actualizado",
        examples={
            "application/json": {"message": "Usuario actualizado"}
        }
    ),
    400: openapi.Response(
        description="Error de validación",
        examples={
            "application/json": {
                "message": "Ya existe un usuario con este email"
            }
        }
    ),
    404: openapi.Response(
        description="Usuario no encontrado",
        examples={
            "application/json": {"message": "Usuario no encontrado"}
        }
    ),
}

update_user_params =[
    openapi.Parameter(
        'id', 
        openapi.IN_PATH, 
        description="ID de usuario", 
        type=openapi.TYPE_INTEGER,
        required=True
    )
]

delete_user_responses = {
    200: openapi.Response(
        description="Usuario eliminado",
        examples={
            "application/json": {"message": "Usuario eliminado"}
        }
    ),
    400: openapi.Response(
        description="Error de validación",
        examples={
            "application/json": {
                "message": "Estado enviado invalido"
            }
        }
    ),
    404: openapi.Response(
        description="Usuario no encontrado",
        examples={
            "application/json": {"message": "Usuario no encontrado"}
        }
    ),
}