from django.urls import path
from accounts.views import UserRegisterView, UserLoginView, UserLogoutView, AdminLoginView, \
    AdminLogoutView, ProfileUpdateView, ProfileView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),

    path('admin-login/', AdminLoginView.as_view(), name='admin_login'),
    path('admin-logout/', AdminLogoutView.as_view(), name='admin_logout'),
]