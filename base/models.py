from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.utils import timezone


class Task(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    todo = models.CharField(max_length=100,null=True,blank=False)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.complete:
            self.updated = timezone.now()
        super().save(*args, **kwargs)

    def _str__(self):
        return self.todo