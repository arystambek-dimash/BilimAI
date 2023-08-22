from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics
from . import models
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer, UserProfileSerializer, ChatHistorySerizlizer


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer


class UserProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChatQueryView(generics.CreateAPIView):
    queryset = models.ChatHistory.objects.all()
    serializer_class = ChatHistorySerizlizer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user_query = request.data.get('content')

        gpt_response = "Hello World"

        chat_history = models.ChatHistory(content=user_query, chat_answer=gpt_response,user=request.user)
        chat_history.save()

        serializer = ChatHistorySerizlizer(chat_history)

        return Response({
            "serializer":serializer.data,
            "chat_answer":gpt_response
        })
