from django.urls import path
from .views import RegisterUserView, CreateGetAllUserView, UpdateGetDeleteUserView, LoginView, PasswordResetEmailView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register_users'),
    path('user/', CreateGetAllUserView.as_view(), name='create_list_users'),
    path('user/<int:id>/', UpdateGetDeleteUserView.as_view(), name='retrieve_update_delete_user'),
    path('login/', LoginView.as_view(), name='login_user'),
    path('password-email/', PasswordResetEmailView.as_view(), name='password_email')
]