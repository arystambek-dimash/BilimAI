from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('accounts/profile/', views.UserProfileView.as_view(), name='profile'),
    path('chat/',views.ChatQueryView.as_view())
]