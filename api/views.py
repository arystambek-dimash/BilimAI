import os
import secrets

import django_filters
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from rest_framework.decorators import permission_classes
from rest_framework import generics
from . import models, filter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer, UserProfileSerializer, ChatHistorySerizlizer, \
    ChatHistorySerizlizerGET, CourseSerializer, CourseVideoSerializer, VideoMaterialSerializer, TestSerializer, TestSerializerGET
from gpt_config import chat_query
from gpt_test_config import test_query
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters
from .models import Test, Question, QuestionOption
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


############################### USER ###########################################
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


############################ CHAT ######################################
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

    def list(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated:
            queryset = models.ChatHistory.objects.filter(user=user)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({"USER": "UNAUTHORIZED"}, status=status.HTTP_401_UNAUTHORIZED)


class ChatHistoryDetailDelete(generics.RetrieveDestroyAPIView):
    queryset = models.ChatHistory.objects.all()
    serializer_class = ChatHistorySerizlizerGET
    permission_classes([IsAuthenticated])

    def get_object(self):
        pk = self.kwargs.get('pk')
        try:
            chat_history = self.queryset.get(pk=pk)
            if self.request.user == chat_history.user:
                return chat_history
            else:
                return
        except models.ChatHistory.DoesNotExist:
            return


############################### TEST ###########################################
class TestCreateView(generics.CreateAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated]


    def create(self, request, *args, **kwargs):
        my_text = request.data.get('my_text')
        if my_text is None:
            return Response({'error': 'my_text is required'}, status=status.HTTP_400_BAD_REQUEST)

        question_title = Test.objects.create(my_text=my_text, user=request.user)

        questions = test_query(my_text)
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
            opt = QuestionOption.objects.create(question=q, text=a, is_correct=True)
            opt1 = QuestionOption.objects.create(question=q, text=b)
            opt2 = QuestionOption.objects.create(question=q, text=c)
            opt3 = QuestionOption.objects.create(question=q, text=d)

        serializer = TestSerializer(question_title)
        return Response(serializer.data)


class TestAll(generics.ListAPIView):
    serializer_class = TestSerializerGET
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Test.objects.filter(user=self.request.user)


class TestDeleteView(generics.RetrieveDestroyAPIView):
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Test.objects.filter(user=self.request.user)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'status': 'Test deleted'}, status=status.HTTP_204_NO_CONTENT)

############################### COURSE ###########################################
class CoursesListView(generics.ListAPIView):
    queryset = models.Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ["name"]
    ordering_fields = ["price", "name"]
    filter_class = filter.CourseFilter

    def get_queryset(self):
        queryset = models.Course.objects.all()
        choices_param = self.request.query_params.get('category')
        if choices_param:
            category = str(choices_param).lower().capitalize()
            queryset = queryset.filter(category=category)

        return queryset


class CourseQueryView(generics.CreateAPIView):
    queryset = models.Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            image = request.data.get("img")
            if image:
                image_name = f"{secrets.token_hex(10)}.{image.name.split('.')[-1]}"
                image_path = os.path.join("media/images", image_name)
                with open(image_path, "wb") as image_file:
                    for chunk in image.chunks():
                        image_file.write(chunk)
                serializer.validated_data["img"] = image_path.replace("media/", "")
            category = request.data.get("category")
            if category == "Free":
                serializer.validated_data["price"] = 0
            if category == "Paid":
                group_name = serializer.validated_data.get("name")
                try:
                    existing_group = Group.objects.get(name=group_name)
                except Group.DoesNotExist:
                    new_group = Group(name=group_name)
                    new_group.save()
            serializer.save(user=request.user)
        return Response({"serializer": serializer.data, "user": request.user.username})


class CourseDeleteView(generics.RetrieveDestroyAPIView):
    queryset = models.Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        pk = self.kwargs.get("pk")
        try:
            course = self.queryset.get(pk=pk)
            if self.request.user == course.user:
                course.delete()
                return course
        except models.Course.DoesNotExist:
            return


############################### COURSE_VIDEO ###########################################
class CourseVideosView(generics.ListAPIView):
    serializer_class = CourseVideoSerializer

    def get_queryset(self):
        course_id = self.kwargs.get("pk")
        queryset = models.CourseVideo.objects.filter(course=course_id)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        custom_data = [
            {
                "id": item["id"],
                "name": item["name"],
                "date_uploaded": item["date_uploaded"]
            }
            for item in serializer.data
        ]

        return Response(custom_data)


class CourseVideoQueryView(generics.CreateAPIView):
    queryset = models.VideoMaterial.objects.all()
    serializer_class = CourseVideoSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        course_id = kwargs.get("pk")
        course = models.Course.objects.get(pk=course_id)
        if course and course.user == request.user:
            serializer = CourseVideoSerializer(data=request.data)
            if serializer.is_valid():
                content = request.data.get("content")
                content_name = f"{secrets.token_hex(5)}.{content.name.split('.')[-1]}"
                content_path = os.path.join("media/videos", content_name)
                with open(content_path, "wb") as content_file:
                    for chunk in content.chunks():
                        content_file.write(chunk)
                serializer.validated_data["content"] = content_path.replace("media/", "")
                serializer.save(course=course)
                return Response(serializer.data)
            return Response({"valid contains": 'MOV,avi,mp4,webm,mkv'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response("You don't have a course with this ID")


class CourseVideoDetail(generics.RetrieveAPIView):
    serializer_class = CourseVideoSerializer

    def get_object(self):
        course_id = self.kwargs.get("pk")
        video_id = self.kwargs.get("video_id")
        user = self.request.user
        try:
            instance_course = models.Course.objects.get(pk=course_id)
            instance_video = models.CourseVideo.objects.get(pk=video_id, course_id=course_id)
            if instance_course.category == "Paid":
                if user.is_authenticated and user.groups.filter(name=instance_course.name).exists():
                    return instance_video
                else:
                    return None
            return instance_video
        except models.Course.DoesNotExist or models.CourseVideo.DoesNotExist:
            return None
