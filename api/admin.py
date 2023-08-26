from django.contrib import admin
from .models import ChatHistory, Test, Question, QuestionOption
# Register your models here.


admin.site.register(ChatHistory)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(QuestionOption)