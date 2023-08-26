from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics
from . import models
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer, UserProfileSerializer, ChatHistorySerizlizer, \
    ChatHistorySerizlizerGET
from gpt_config import chat_query
import translators as ts


from .serializers import TestSerializer
from gpt_test_config import test_query

from rest_framework import status
from .models import Test, Question, QuestionOption



class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        response = super(UserRegistrationView, self).create(request, *args, **kwargs)
        if response.status_code == 201:
            return HttpResponseRedirect('/api/auth/login/')
        return response


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
        gpt_response = chat_query(user_query)
        chat_history = models.ChatHistory(content=user_query, chat_answer=gpt_response, user=request.user)
        chat_history.save()

        serializer = ChatHistorySerizlizer(chat_history)

        return Response({
            "serializer": serializer.data,
            "chat_answer": gpt_response
        })




class ChatHistoryAll(generics.ListAPIView):
    queryset = models.ChatHistory.objects.all()
    serializer_class = ChatHistorySerizlizerGET
    permission_classes([IsAuthenticated])


class ChatHistoryDetailDelete(generics.RetrieveDestroyAPIView):
    queryset = models.ChatHistory.objects.all()
    serializer_class = ChatHistorySerizlizerGET
    permission_classes([IsAuthenticated])




class TestCreateView(generics.CreateAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        my_text = data.get('my_text')
        questions = test_query(my_text)

        formatted_data = {
            "my_text": my_text,
            "questions": questions
        }

        # print(formatted_data)

        serializer = self.get_serializer(data=formatted_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

