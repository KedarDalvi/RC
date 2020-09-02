from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', signup, name = 'signup'),
    path('SignIn/', signin, name = 'signin'),
    path('home/', home,  name = 'home'),
    path('logout/', logout, name = 'logout'),
    path('quiz/', quiz, name ='quiz')
]
