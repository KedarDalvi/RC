from django.db import models

from django.db import models
from django.contrib.auth.models import User

class details(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    ph_no=models.IntegerField()
    year=models.CharField(max_length=10)
    score=models.IntegerField(default=0)


    def __str__(self):
        return self.user.username

    
class Question(models.Model):
    question=models.TextField()
    level=models.CharField(max_length=20)
    answer = models.IntegerField(default=000)

class Response(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    first_attempt=models.IntegerField()
    second_attempt=models.IntegerField()
    participant=models.ForeignKey(User,on_delete=models.CASCADE)
