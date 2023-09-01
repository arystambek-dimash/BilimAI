from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator

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
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


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
    price = models.IntegerField(validators=[
        MinValueValidator(10),
        MaxValueValidator(10000),
    ])
    created_data = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kaspi_gold = PhoneNumberField(null=True)


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


class FavoriteCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'course',)


class BuyCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)
    summa = models.IntegerField(
        validators=[
            MinValueValidator(10),
            MaxValueValidator(10000),
        ]
    )

    def __str__(self):
        return f"{self.user.username} purchased {self.course.name} on {self.purchase_date}"


class MyCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)


class CourseImage(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', null=False)
    description = models.TextField(blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)