from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import auth

urlpatterns = [
    path('register/', auth.register_user, name='register'),
    path('login/', auth.login_user, name='login'),
    path('logout/', auth.logout_user, name='logout'),
    path('token/', auth.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', auth.UserProfileView.as_view(), name='user_profile'),
]
