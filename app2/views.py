from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .models import details
from django.core.validators import validate_email
from django.contrib.auth import login ,logout ,authenticate
import re
from django.http import HttpResponse
from .models import Question


def signup(request):
    if request.method=="POST":
        username_regex='^(?=.{4,20}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$'
        email_regex='^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        mistake=0
        data=request.POST
        username=data['username']
        f_name=data['fname']
        l_name=data['lname']
        email=data['email']
        ph_no=data['mob']
        password = data['password1']
        if (re.search(username_regex,username)== None ):
            messages.info(request,'Enter the valid username!')
            mistake=1
        if f_name.isalpha()==False:
            messages.info(request,"Enter the correct First name!")
            mistake=1
        if l_name.isalpha()==False:
            messages.info(request,"Enter the correct Last name!")
            mistake=1
        if (re.search(email_regex,email) ==None):
            messages.info(request,"Enter a valid email address")
            mistake=1
        if ((ph_no.isdigit()==False) or (len(str(ph_no))!=10) or ((str(ph_no)[0] in ['0','1','2','3','4','5'])==True)):
            messages.info(request,'Enter a valid phone number')
            mistake=1
        if mistake==1:
            return render(request,'app2/signup.html')        
        else:
            if data['password1']==data['password2']:
                try:
                    user=User.objects.create_user(username=username,first_name=f_name,last_name=l_name,email=email,password=password)
                    profile=details(user=user,ph_no=ph_no)
                    profile.save()
                    messages.info(request,'User Registered successfully!')
                    return render(request,'app2/signup.html')
                except:
                    messages.info(request,'User already exist')
                    return render(request,'app2/signup.html')
            messages.info(request, 'Passwords do not match ')
            return render(request,'app2/signup.html')       
    if request.method=="GET":
        return render(request,'app2/signup.html')

def signin(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return render(request,'app2/success.html',{'user':user})
        else:
            messages.info(request,'Invalid Credentials')
            return render(request,'app2/signin.html',)
    if request.method=="GET":
        return render(request,'app2/signin.html',)

def success(request):
    context={}
    context['questions']=Question.objects.all()
    return render(request,'app2/success.html',context)

def logout(request):
    
    auth.logout(request)
    messages.info(request,'Successfully logged out!')
    return render(request,'app2/signin.html')

