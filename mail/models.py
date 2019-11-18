from django.db import models
from django.utils import timezone

from django.contrib.auth import get_user_model


class Mail(models.Model):
    author = models.ForeignKey(get_user_model(),
                               null=True,
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    email = models.CharField(max_length=200)
    status = models.BooleanField()

    def __str__(self):
        return self.title
