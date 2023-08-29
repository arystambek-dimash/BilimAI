from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User

CHOICES = (
    ("Free", "Free"),
    ("Paid", "Paid"),
)


class ChatHistory(models.Model):
    content = models.TextField()
    chat_answer = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class Test(models.Model):
    my_text = models.TextField()


class Question(models.Model):
    test = models.ForeignKey(Test, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()


class QuestionOption(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)


class Course(models.Model):
    img = models.ImageField(upload_to="images/", null=True)
    name = models.CharField(null=False, max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=4, choices=CHOICES)
    price = models.IntegerField(default=0)
    created_data = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class CourseVideo(models.Model):
    name = models.CharField(max_length=255, null=False)
    content = models.FileField(upload_to="videos/", null=False,
                               validators=
                               [FileExtensionValidator(
                                   ['MOV', 'avi', 'mp4', 'webm', 'mkv'])])

    date_uploaded = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class VideoMaterial(models.Model):
    file = models.FileField(upload_to="materials/", null=True,
                            validators=[FileExtensionValidator(allowed_extensions=["txt", "pdf", "docs"])])
    course_video = models.ForeignKey(CourseVideo, on_delete=models.CASCADE)
