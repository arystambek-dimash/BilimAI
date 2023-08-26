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
        my_text = request.data.get('my_text')
        if my_text is None:
            return Response({'error': 'my_text is required'}, status=status.HTTP_400_BAD_REQUEST)

        question_title = Test.objects.create(my_text=my_text)

        questions = test_query(my_text)
        print(questions)
        if questions is None or not isinstance(questions, list):
            return Response({'error': 'Invalid questions data'}, status=status.HTTP_400_BAD_REQUEST)

        for ques in questions:
            question = ques.get("question")
            options = ques.get("options")
            a = options.get("A")
            b = options.get("B")
            c = options.get("C")
            d = options.get("D")
            correct_answer = ques.get("correct_answer")

            q = Question.objects.create(test=question_title, text=question)
            opt = QuestionOption.objects.create(question=q, text=a,is_correct=True)
            opt1 = QuestionOption.objects.create(question=q, text=b)
            opt2 = QuestionOption.objects.create(question=q, text=c)
            opt3 = QuestionOption.objects.create(question=q, text=d)

        serializer = TestSerializer(question_title)
        return Response(serializer.data)