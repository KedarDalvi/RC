from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .models import details
from django.core.validators import validate_email
from django.contrib.auth import login ,logout ,authenticate
import re
from django.http import HttpResponse


def signup(request):
    if request.method=="POST":
        username=request.POST['username']
        regex1='^[a-zA-Z0-9]+([._]?[a-zA-Z0-9]+)$'
        if (re.search(regex1,username)== None ):
            messages.info(request,'Enter the valid username!')
            return render(request,'app2/signup.html')
        else:
            f_name=request.POST['fname']
            l_name=request.POST['lname']
            if f_name.isalpha()==False:
                messages.info(request,"Enter the correct First name!")
                return render(request,'app2/signup.html')
            elif l_name.isalpha()==False:
                messages.info(request,"Enter the correct Last name!")
                return render(request,'app2/signup.html')
            else:
                email=request.POST['email']
                regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
                if (re.search(regex,email) ==None):
                    messages.info(request,"Enter a valid email address")
                    return render(request,'app2/signup.html')
                else:
                    ph_no=request.POST['mob']
                    if ((ph_no.isdigit()==False) or (len(str(ph_no))!=10) or ((str(ph_no)[0] in ['0','1','2','3','4','5'])==True)):
                        messages.info(request,'Enter a valid phone number')
                        return render(request,'app2/signup.html')
                    else:
                        if request.POST['password1']==request.POST['password2']:
                            password = request.POST['password1']
                            regex_password="^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[*.!@$%^&(){}[]:;<>,.?/~_+-=|\]).{8,32}$"
                            if (re.search(regex_password,password) ==None):
                                messages.info(request,"Enter strong  password ")
                                return render(request,'app2/signup.html')
                            else:       
                                try:
                                    user=User.objects.create_user(username=username,first_name=f_name,last_name=l_name,email=email,password=password)
                                    profile=details(user=user,ph_no=ph_no)
                                    profile.save()
                                    user = auth.authenticate(username=username,password=password)
                                    login(request,user)
                                    messages.info(request,'user created!')
                                    return redirect('success')
                                except:
                                    messages.info(request,'User already exist')
                                    return render(request,'app2/signup.html',)
                        else:
                            messages.info(request, 'Passwords do not match :)')
                            return render(request,'app2/signup.html',)
    if request.method=="GET":
        return render(request,'app2/signup.html')

def signin(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('success')
        else:
            messages.info(request,'Invalid Credentials')
            return render(request,'app2/signin.html',)
    if request.method=="GET":
        return render(request,'app2/signin.html',)

def success(request):
    data=details.objects.get(user=request.user)
    return render(request,'app2/success.html',{'data':data})


def logout(request):
    auth.logout(request)
    messages.info(request,'Successfully logged out!')
    return render(request,'app2/signin.html')




