from django.urls import path
from . import views
from .views import TestCreateView

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('accounts/profile/', views.UserProfileView.as_view(), name='profile'),
    path('chat/',views.ChatQueryView.as_view()),
    path('chat/history/',views.ChatHistoryAll.as_view()),
    path('chat/history/<int:pk>/delete/', views.ChatHistoryDetailDelete.as_view()),
    path('test/', TestCreateView.as_view(), name='create-test'),

]