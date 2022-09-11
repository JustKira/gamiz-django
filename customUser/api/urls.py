
from unicodedata import name
from django.urls import path
from . import views
from .views import MyTokenObtainPairView
from django.urls import path, include

from rest_framework_simplejwt.views import(
    TokenRefreshView,
)

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name="token_obtian_pair"),
    path('token/refresh', TokenRefreshView.as_view(), name="token_refresh"),
    path('user/<pk>', views.getUser, name="user"),
    path('resend-verify-email/', views.resendEmailVerifcation,
         name="resend-verify-email"),
    #    path('email/<str:token>/', views.confirm),
    path('change-password/', views.ChangePasswordView.as_view(),
         name='change-password'),
    path('password_reset/', include('django_rest_passwordreset.urls',
         namespace='password_reset')),
    path('verify-email/', views.VerifyEmail.as_view(), name="verify-email"),
    path('user-create', views.userCreate, name="user-create"),
    path('user-update/<pk>', views.userUpdate, name="user-update"),
    path('user-delete/<pk>', views.userDelete, name="user-delete")
]
