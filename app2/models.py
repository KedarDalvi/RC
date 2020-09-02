from django.db import models
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User

class details(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    ph_no = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    year=models.CharField(max_length=10)
    score=models.IntegerField(default=0)


    def __str__(self):
        return self.user.username

    
class Question(models.Model):
    question=models.TextField()
    level=models.CharField(max_length=20)
    answer = models.IntegerField(default=000)
    def __str__(self):
        return self.question


class Response(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    first_attempt=models.IntegerField()
    second_attempt=models.IntegerField()
    participant=models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username
