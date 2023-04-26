from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


class Feedback(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField(max_length=500)
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE, default=0)
    date = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return f'({self.user}) {self.title}'
