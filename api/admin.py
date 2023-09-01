from django.contrib import admin
from .models import ChatHistory, Test, Question, QuestionOption,Course,CourseVideo,VideoMaterial, FavoriteCourse, MyCourse
# Register your models here.


admin.site.register(ChatHistory)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(QuestionOption)
admin.site.register(Course)
admin.site.register(CourseVideo)
admin.site.register(VideoMaterial)
admin.site.register(FavoriteCourse)
admin.site.register(MyCourse)