from django.urls import path, include
from api.views import VerifyTokenView, VerifyIntraTokenView, HealthCheckView
from api.views import ForgotPasswordView, ChangePasswordView, ResetPasswordView
from api.views import RegisterView, IntraRegisterView,LoginView, LoginRefrechView, LogoutView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='token_obtain_pair'),
    path('auth/login/refresh/', LoginRefrechView.as_view(), name='token_refresh'),
    path('auth/logout/', LogoutView.as_view(), name='token_blacklist'),
    path('auth/intra/register/', IntraRegisterView.register, name='intra_token'),
    path('auth/intra/redirect/', IntraRegisterView.register_process, name='intra_register'),
    path('auth/verify/', VerifyTokenView.as_view(), name='verify_token'),
    path('auth/intra/verify/', VerifyIntraTokenView.as_view(), name='verify_token'),
    path('auth/password/reset/', ResetPasswordView.as_view(), name='reset_password'),
    path('auth/password/forgot/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('auth/password/change/', ChangePasswordView.as_view(), name='change_password'),
    path('auth/health/', HealthCheckView.as_view(), name='health_check'),
    path('', include('django_prometheus.urls')),
]
