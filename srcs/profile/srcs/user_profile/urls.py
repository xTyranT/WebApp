from django.urls import path
from api.views import CreateIntraProfileView, CreateProfileView, GetProfileView, GetProfileByIdView, UpdateProfileView, SearchProfile
from api.views import SendFriendRequestView, AcceptFriendRequestView, RejectFriendRequestView, FriendListView, HealthCheckView, FriendRequestListView

urlpatterns = [
    path('profile/intra/create/', CreateIntraProfileView.as_view(), name='intra_profile'),
    path('profile/create/', CreateProfileView.as_view(), name='profile'),
    path('profile/me/', GetProfileView.as_view(), name='get_profile'),
    path('profile/<int:id>', GetProfileByIdView.as_view(), name='get_profile_by_id'),
    path('profile/update/', UpdateProfileView.as_view(), name='update_profile'),
    path('profile/friend/request/<int:rid>', SendFriendRequestView.as_view(), name='friend_request'),
    path('profile/friend/accept/<int:sid>', AcceptFriendRequestView.as_view(), name='friend_accept'),
    path('profile/friend/reject/<int:sid>', RejectFriendRequestView.as_view(), name='friend_accept'),
    path('profile/friend/request/list/', FriendRequestListView.as_view(), name='friend_request_list'),
    path('profile/friend/list/', FriendListView.as_view(), name='friends_list'),
    path('profile/search/<query>', SearchProfile.as_view(), name='search_profile'),
    path('profile/health/', HealthCheckView.as_view(), name='health_check'),
]
