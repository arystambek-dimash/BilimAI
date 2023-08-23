from django.db import models
from django.contrib.auth.models import User


class ChatHistory(models.Model):
    content = models.TextField()
    chat_answer = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


