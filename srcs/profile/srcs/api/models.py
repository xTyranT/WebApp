from django.db import models

class ProfileManager(models.Manager):
    def create_profile(self, id, nickname=None, avatar=None, avatar_url=None):
        if avatar is None and not avatar_url:
            avatar = 'default.jpg'
        user_profile = self.model(
            id=id,
            nickname=nickname,
            avatar=avatar,
            avatar_url=avatar_url,
        )
        user_profile.save(using=self._db)
        return user_profile

class Profile(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(upload_to='uploads/', default='default.jpg')
    avatar_url = models.URLField(blank=True, null=True)
    friendships = models.ManyToManyField("self", blank=True, through='FriendRequest', symmetrical=False)
    objects = ProfileManager()

class FriendRequest(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')
    
    class Meta:
        unique_together = ('sender', 'receiver')