from .models import Profile, FriendRequest
from rest_framework import serializers
from django.db import models

class ProfileSerializer(serializers.ModelSerializer):
    friendships = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = ('id', 'nickname', 'avatar', 'avatar_url', 'friendships')
    
    def get_friends(profile):
        friendships = FriendRequest.objects.filter(
            (models.Q(sender=profile) | models.Q(receiver=profile)),
            status='accepted'
        )
        friends = [
            {
                'id': f.receiver.id if f.sender == profile else f.sender.id,
                'nickname': f.receiver.nickname if f.sender == profile else f.sender.nickname,
                'avatar': (
                    f.receiver.avatar_url if f.receiver.avatar is not None 
                        else f.receiver.avatar.url)
                    if f.sender == profile else (
                        f.sender.avatar_url if f.sender.avatar_url is not None 
                            else f.sender.avatar.url)
            }
            for f in friendships
        ]
        return friends

    def create(self, validated_data):
        profile = Profile.objects.create_profile(**validated_data)
        return profile