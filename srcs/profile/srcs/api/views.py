import urllib3
import requests, json
from rest_framework import status
from rest_framework import generics
from django.http import JsonResponse
from .models import Profile, FriendRequest
from .serializers import ProfileSerializer
from rest_framework.permissions import AllowAny

urllib3.disable_warnings()

class CreateIntraProfileView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    http_method_names = ['post']
    
    def post(self, request):
        auth_token = request.headers.get("Authorization")
        auth_server_url = "https://nginx/auth/intra/verify/"
        headers = {"Authorization": auth_token}
        response = requests.get(auth_server_url, headers=headers, verify=False)
        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            id = data.get("id")
            nickname = data.get("username")
            avatar_url = data.get("avatar")
            avatar = None
            try:
                Profile.objects.create_profile(id=id, nickname=nickname, avatar=avatar, avatar_url=avatar_url)
                return JsonResponse(data, status=status.HTTP_201_CREATED, safe=False)
            except:
                return JsonResponse({"error": "profile already exists"}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({"my error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    
class CreateProfileView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    http_method_names = ['post']

    def post(self, request):
        auth_token = request.headers.get("Authorization")
        auth_server_url = "https://nginx/auth/verify/"
        headers = {"Authorization": auth_token}
        response = requests.get(auth_server_url, headers=headers, verify=False)
        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            id = data.get("id")
            nickname = data.get("username")
            avatar = None
            try:
                Profile.objects.create_profile(id=id, nickname=nickname, avatar=avatar)
                return JsonResponse("profile created successfully", status=status.HTTP_201_CREATED, safe=False)
            except:
                return JsonResponse({"error": "profile already exists"}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

class GetProfileView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    http_method_names = ['get']
    
    def get(self, request):
        auth_token = request.headers.get("Authorization")
        auth_server_url = "https://nginx/auth/verify/"
        headers = {"Authorization": auth_token}
        response = requests.get(auth_server_url, headers=headers, verify=False)
        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            id = data.get("id")
            profile = Profile.objects.get(id=id)
            nickname = profile.nickname
            if profile.avatar:
                avatar = profile.avatar.url
            else:
                avatar = profile.avatar_url
            friends = ProfileSerializer.get_friends(profile)
            data = {
                "id": id,
                "nickname": nickname,
                "avatar": avatar,
                "friendships": friends
            }
            return JsonResponse(data, status=status.HTTP_200_OK, safe=False)
        return JsonResponse({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

class GetProfileByIdView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    http_method_names = ['get']
    
    def get(self, request, id):
        auth_token = request.headers.get("Authorization")
        auth_server_url = "https://nginx/auth/verify/"
        headers = {"Authorization": auth_token}
        response = requests.get(auth_server_url, headers=headers, verify=False)
        if response.status_code == status.HTTP_200_OK:
            try:
                profile = Profile.objects.get(id=id)
                data = {
                    "id": profile.id,
                    "nickname": profile.nickname,
                    "avatar": profile.avatar.url if profile.avatar else profile.avatar_url,
                    "friendships": ProfileSerializer.get_friends(profile)
                }
                return JsonResponse(data, status=status.HTTP_200_OK, safe=False)
            except:
                return JsonResponse({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        return JsonResponse({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

class UpdateProfileView(generics.UpdateAPIView):
    permission_classes = [AllowAny]
    http_method_names = ['put']

    def put(self, request):
        auth_token = request.headers.get("Authorization")
        auth_server_url = "https://nginx/auth/verify/"
        headers = {"Authorization": auth_token}
        response = requests.get(auth_server_url, headers=headers, verify=False)
        if response.status_code == status.HTTP_200_OK:
            id = response.json().get("id")
            try:
                profile = Profile.objects.get(id=id)
                if 'nickname' in request.data:
                    profile.nickname = request.data.get('nickname')
                if 'avatar' in request.FILES:
                    profile.avatar = request.FILES['avatar']
                    profile.avatar_url = None
                profile.save()
                return JsonResponse({"message": "Profile updated successfully"}, status=status.HTTP_200_OK)
            except Profile.DoesNotExist:
                return JsonResponse({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        return JsonResponse({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

class SendFriendRequestView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    http_method_names = ['post']
    
    def post(self, request, rid):
        auth_token = request.headers.get("Authorization")
        auth_server_url = "https://nginx/auth/verify/"
        headers = {"Authorization": auth_token}
        response = requests.get(auth_server_url, headers=headers, verify=False)
        if response.status_code == status.HTTP_200_OK:
            sid = response.json().get("id")
            sender = Profile.objects.get(id=sid)
            receiver = Profile.objects.get(id=rid)
            if sid == rid:
                return JsonResponse({"error": "You cannot send friend request to yourself."}, status=status.HTTP_400_BAD_REQUEST)
            friend_request, created = FriendRequest.objects.get_or_create(sender=sender, receiver=receiver)
            if created:
                return JsonResponse({"message": "Friend request sent."}, status=status.HTTP_201_CREATED)
            return JsonResponse({"error": "Friend request was already sent."}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)

class AcceptFriendRequestView(generics.UpdateAPIView):
    permission_classes = [AllowAny]
    http_method_names = ['put']
    
    def put(self, request, sid):
        auth_token = request.headers.get("Authorization")
        auth_server_url = "https://nginx/auth/verify/"
        headers = {"Authorization": auth_token}
        response = requests.get(auth_server_url, headers=headers, verify=False)
        if response.status_code == status.HTTP_200_OK:
            friend_request = FriendRequest.objects.get(sender=sid, receiver=response.json().get("id"))
            if not friend_request:
                return JsonResponse({"error": "Friend request not found."}, status=status.HTTP_404_NOT_FOUND)
            friend_request.status = 'accepted'
            friend_request.save()
            return JsonResponse({"message": "Friend request accepted."}, status=status.HTTP_200_OK)
        return JsonResponse("Unauthorized", status=status.HTTP_401_UNAUTHORIZED, safe=False)

class RejectFriendRequestView(generics.UpdateAPIView):
    permission_classes = [AllowAny]
    http_method_names = ['put']
    
    def put(self, request, sid):
        auth_token = request.headers.get("Authorization")
        auth_server_url = "https://nginx/auth/verify/"
        headers = {"Authorization": auth_token}
        response = requests.get(auth_server_url, headers=headers, verify=False)
        if response.status_code == status.HTTP_200_OK:
            friend_request = FriendRequest.objects.get(sender=sid, receiver=response.json().get("id"))
            if not friend_request:
                return JsonResponse({"error": "Friend request not found."}, status=status.HTTP_404_NOT_FOUND)
            friend_request.status = 'rejected'
            friend_request.save()
            return JsonResponse({"message": "Friend request rejected."}, status=status.HTTP_200_OK)
        return JsonResponse("Unauthorized", status=status.HTTP_401_UNAUTHORIZED, safe=False)

class FriendRequestListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    http_method_names = ['get']
    
    def get(self, request):
        auth_token = request.headers.get("Authorization")
        auth_server_url = "https://nginx/auth/verify/"
        headers = {"Authorization": auth_token}
        response = requests.get(auth_server_url, headers=headers, verify=False)
        if response.status_code == status.HTTP_200_OK:
            uid = response.json().get("id")
            profile = Profile.objects.get(id=uid)
            friend_requests = FriendRequest.objects.filter(receiver=profile, status='pending')
            data = []
            for request in friend_requests:
                data.append({
                    "id": request.id,
                    "sender": request.sender.nickname,
                    "avatar": request.sender.avatar.url if request.sender.avatar else request.sender.avatar_url
                })
            return JsonResponse(data, status=status.HTTP_200_OK, safe=False)
        return JsonResponse("Unauthorized", status=status.HTTP_401_UNAUTHORIZED, safe=False)

class FriendListView(generics.ListAPIView):
    permssion_classes = [AllowAny]
    http_method_names = ['get']
    
    def get(self, request):
        auth_token = request.headers.get("Authorization")
        auth_server_url = "https://nginx/auth/verify/"
        headers = {"Authorization": auth_token}
        response = requests.get(auth_server_url, headers=headers, verify=False)
        if response.status_code == status.HTTP_200_OK:
            uid = response.json().get("id")
            profile = Profile.objects.get(id=uid)
            friends = ProfileSerializer.get_friends(profile)
            return JsonResponse(friends, status=status.HTTP_200_OK, safe=False)
        return JsonResponse("Unauthorized", status=status.HTTP_401_UNAUTHORIZED, safe=False)

class SearchProfile(generics.ListAPIView):
    permission_classes = [AllowAny]
    http_method_names = ['get']
    
    def get(self, request, query):
        auth_token = request.headers.get("Authorization")
        auth_server_url = "https://nginx/auth/verify/"
        headers = {"Authorization": auth_token}
        response = requests.get(auth_server_url, headers=headers, verify=False)
        if response.status_code == status.HTTP_200_OK:
            profiles = Profile.objects.filter(nickname__icontains=query)
            data = []
            for profile in profiles:
                data.append({
                    "id": profile.id,
                    "nickname": profile.nickname,
                    "avatar": profile.avatar.url if profile.avatar else profile.avatar_url
                })
            return JsonResponse(data, status=status.HTTP_200_OK, safe=False)
        return JsonResponse("Unauthorized", status=status.HTTP_401_UNAUTHORIZED, safe=False)

class HealthCheckView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    http_method_names = ['get']

    def get(self, request):
        return JsonResponse({"status": "ok"}, status=status.HTTP_200_OK)