from django.db import models
from django.contrib.auth.models import User, auth

class UserProfile(models.Model):
    user= models.OneToOneField(User, on_delete = models.CASCADE, max_length = 100)
    phone = models.IntegerField()
    year = models.CharField(max_length=10)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class Question(models.Model):
    question = models.TextField()
    level = models.CharField(max_length = 100)
    correct_ans = models.IntegerField()

    def __str__(self):
        return self.question

class Response( models.Model ) :
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    attempt_1 = models.IntegerField(max_length = None)
    attempt_2 = models.IntegerField(max_length = None)
    no_question_solved = models.IntegerField(default = 0, editable=True)
    current_score = models.IntegerField(default = 0, editable = True)
    question_attempted = models.TextField(default = 0)

    def __str__(self):
        return self.user.username

