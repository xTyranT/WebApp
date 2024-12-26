import os
import urllib3
import requests, json
from .models import CustomUser
from django.conf import settings
from rest_framework import status
from rest_framework import generics
from django.http import JsonResponse
from django.shortcuts import redirect
from django.core.mail import send_mail
from urllib.parse import urlparse, parse_qs
from django.contrib.auth import authenticate
from django.utils.crypto import get_random_string
from django.utils.encoding import force_bytes, force_str
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .serializers import  UserSerializer, LoginSerializer, RefreshTokenSerializer, ResetPasswordSerializer

urllib3.disable_warnings()

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = CustomUser.objects.get(username=serializer.data['username'])
            refresh = RefreshToken.for_user(user)
            tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            profile = requests.post("https://nginx/profile/create/", headers={"Authorization": f"JWT {tokens['access']}"}, verify=False)
            if profile.status_code == status.HTTP_201_CREATED or profile.status_code == status.HTTP_400_BAD_REQUEST:   
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse({"error": "profile creation failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IntraRegisterView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    http_method_names = ['get']

    def register(request):
        intra_api_url = os.getenv('INTRA_REDIRECT_URI')
        response = redirect(intra_api_url)
        return response
    
    def register_process(request):
        intra_api_url = os.getenv('INTRA_REDIRECT_URI')
        url_parts = urlparse(intra_api_url)
        query_params = parse_qs(url_parts.query)
        token_url = "https://api.intra.42.fr/oauth/token"
        request_query_params = request.GET
        client_secret = os.getenv('INTRA_SECRET')
        code = request_query_params.get("code", None)
        client_id = query_params.get("client_id", [None])[0]
        redirect_uri = query_params.get("redirect_uri", [None])[0]
        grant_type = "authorization_code"
        state = get_random_string(length=32)
        params = {
            "grant_type": grant_type,
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "redirect_uri": redirect_uri,
            "state": state,
        }
        req = requests.post(token_url, data=params)
        if req.status_code != 200:
            return JsonResponse({"error": "Invalid code"}, status=status.HTTP_401_UNAUTHORIZED)
        user_json = requests.get("https://api.intra.42.fr/v2/me",
            headers={"Authorization": f"Bearer {json.loads(req.content)['access_token']}"})
        user_data = json.loads(user_json.content)
        email = user_data.get('email')
        username = user_data.get('login')
        image = user_data.get('image')
        avatar = image.get('link')
        try:
            user = CustomUser.objects.get(username=username)
        except:
            user = CustomUser.objects.create_user(email=email, username=username, avatar=avatar)
        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        profile = requests.post("https://nginx/profile/intra/create/", headers={"Authorization": f"JWT {tokens['access']}"}, verify=False)
        if profile.status_code == status.HTTP_201_CREATED or profile.status_code == status.HTTP_400_BAD_REQUEST:
            response = JsonResponse(tokens, status=status.HTTP_201_CREATED)
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                value=tokens['access'],
                expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )
        else:
            response = JsonResponse({"error": "profile creation failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response
    
class LoginView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post']
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data['username']
            password = serializer.data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                tokens = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                response = JsonResponse(tokens, status=status.HTTP_200_OK)
                response.set_cookie(
                    key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                    value=tokens['access'],
                    expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
                return response
            return JsonResponse({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    
class LoginRefrechView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RefreshTokenSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post']
    
    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        if serializer.is_valid():
            refresh_token = serializer.data['refresh']
            try:
                refresh = RefreshToken(refresh_token)
                access_token = str(refresh.access_token)
                response = JsonResponse({'message': "access token updated"}, status=status.HTTP_200_OK)
                response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                value=access_token,
                expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
            except Exception:
                response = JsonResponse({"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)
            return response
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = ['put']
    
    def put(self, request):
        user = request.user
        data = request.data
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        if not user.check_password(old_password):
            return JsonResponse({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
        if old_password == new_password :
            return JsonResponse({"error": "New password must be different from old password"}, status=status.HTTP_400_BAD_REQUEST)
        if new_password == confirm_password:
            user.set_password(new_password)
            user.save()
            return JsonResponse({"message": "password changed successfully"}, status=status.HTTP_200_OK)
        return JsonResponse({"error": "passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    http_method_names = ['post']
    
    def post(self, request):
        data = json.loads(request.body)
        email = data.get('email')
        user = CustomUser.objects.get(email=email)
        token = PasswordResetTokenGenerator().make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.id))
        reset_url = f"https://www.transc-net.com/auth/password/reset/?token={token}&uid={uid}"
        send_mail(
            subject="Password Reset Request",
            message=f"Click the link to reset your password: {reset_url}",
            from_email= settings.EMAIL_HOST_USER,
            recipient_list=[email])
        return JsonResponse({"message": "email sent"}, status=status.HTTP_200_OK)

class ResetPasswordView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    http_method_names = ['post']
    serializer_class = ResetPasswordSerializer
    
    def post(self, request):
        try:
            data = request.data
            token = request.GET.get('token')
            uid = request.GET.get('uid')
            decoded_uid = force_str(urlsafe_base64_decode(uid))
            user = CustomUser.objects.get(id=decoded_uid)
            if default_token_generator.check_token(user, token):
                new_password = data.get('new_password')
                confirm_password = data.get('confirm_password')
                if new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()
                    return JsonResponse({"message": "Password reset successfully"}, status=status.HTTP_200_OK)
                return JsonResponse({"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)
            return JsonResponse({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = ['post']
    
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return JsonResponse({"message": "logged out"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return JsonResponse({"message": "logged out"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VerifyTokenView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get']
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        serializer_data = serializer.data
        serializer_data['id'] = request.user.id
        serializer_data.pop('email')
        return JsonResponse(serializer_data, status=status.HTTP_200_OK)

class VerifyIntraTokenView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get']

    def get(self, request):
        serializer = UserSerializer(request.user)
        serializer_data = serializer.data
        serializer_data['id'] = request.user.id
        serializer_data['avatar'] = request.user.avatar
        serializer_data.pop('email')
        return JsonResponse(serializer_data, status=status.HTTP_200_OK)
    
class HealthCheckView(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    http_method_names = ['get']
    
    def get(self, request):
        return JsonResponse({"status": "ok"}, status=status.HTTP_200_OK)
