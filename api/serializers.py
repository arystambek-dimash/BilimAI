from django.contrib.auth.models import User
from .models import ChatHistory, Test, Question, QuestionOption, Course, CourseVideo, VideoMaterial, FavoriteCourse, \
    BuyCourse, MyCourse
from rest_framework import serializers
from phonenumber_field.formfields import PhoneNumberField


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        password2 = validated_data.pop('password2')
        user = super(UserRegistrationSerializer, self).create(validated_data)
        user.set_password(password)
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class ChatHistorySerizlizer(serializers.ModelSerializer):
    class Meta:
        model = ChatHistory
        fields = ("id", "content", "created_date")


class ChatHistorySerizlizerGET(serializers.ModelSerializer):
    class Meta:
        model = ChatHistory
        fields = "__all__"


class QuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ['text', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    options = QuestionOptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ['text', 'options']


class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Test
        fields = ['my_text', 'created_date', 'questions']


class TestSerializerGET(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = "__all__"


class VideoMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoMaterial
        fields = ["file"]


class CourseVideoSerializer(serializers.ModelSerializer):
    course_video = VideoMaterialSerializer(many=True, read_only=True)

    class Meta:
        model = CourseVideo
        fields = ["id", "name", "content", "date_uploaded", "course_video"]


class CourseSerializer(serializers.ModelSerializer):
    course_videos = CourseVideoSerializer(many=True, read_only=True)
    kaspi_gold = PhoneNumberField()

    class Meta:
        model = Course
        fields = ["id", "img", "name", "description", "category", "price", "kaspi_gold", "course_videos"]


class CourseSerializerGET(serializers.ModelSerializer):
    course_videos = CourseVideoSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = "__all__"


class FavoriteCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteCourse
        fields = ['id', 'course']


class FavoriteCourseSerializerGET(serializers.ModelSerializer):
    class Meta:
        model = FavoriteCourse
        fields = "__all__"


class BuyCourseSerializerPOST(serializers.ModelSerializer):
    class Meta:
        model = BuyCourse
        fields = ["name", "summa"]


class BuyCourseSerializerGET(serializers.ModelSerializer):
    class Meta:
        model = BuyCourse
        fields = "__all__"

class MyCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyCourse
        fields = ['id', 'course']

class MyCourseSerializerGET(serializers.ModelSerializer):
    class Meta:
        model = MyCourse
        fields = "__all__"