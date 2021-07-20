from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import (
    CustomTokenObtainPairView,
    UserLogout,
    CreateUser,
    UserCurrent,
    UserDetails)

urlpatterns = [
    path('auth/', include([
        path('', CustomTokenObtainPairView.as_view(), name='token-obtain-pair'),
        path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),
        path('logout/', UserLogout.as_view(), name='logout')
    ])),
    path('create/', CreateUser.as_view(), name='create-user'),
    path('current/', UserCurrent.as_view(), name='current-user'),
    path('<pk>/', UserDetails.as_view(), name='user-details'),
]