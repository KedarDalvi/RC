from django.contrib import admin
from .models import UserProfile, Question, Response

admin.site.register(UserProfile)
admin.site.register(Question)
admin.site.register(Response)