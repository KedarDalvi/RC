from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from userapp.models import UserProfile, Question, Response
import random
import re


def signup(request):
    if request.method == 'GET':
        return render(request, 'SignUp.html')
    else:
        username = request.POST.get('username')
        user_regex = '^(?=.{6,32}$)(?![_.-])(?!.*[_.-]{2})[a-zA-Z0-9._-]+(?<![_.-])$'
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        phone = request.POST.get('phone')
        f_pass = request.POST.get('f_pass')
        c_pass = request.POST.get('c_pass')
        if re.search(user_regex, username) == None:
            return render(request, 'SignUp.html', {'message': 'Enter a valid Username.'})
        if str(first_name).isalpha() == False:
            return render(request, 'SignUp.html', {'message': 'Enter  Correct First Name.'})
        if str(last_name).isalpha() == False:
            return render(request, 'SignUp.html', {'message': 'Enter Correct Last Name'})
        if re.search(email_regex, email) == None:
            return render(request, 'SignUp.html', {'message': 'Enter a valid email id.'})
        if (str(phone).isnumeric() == False) | (int(phone) < 5999999999) | (len(str(phone)) != 10):
            return render(request, 'SignUp.html', {'message': 'Enter Valid Phone number.'})
        if c_pass == f_pass:
            try:
                user = User.objects.get(username=username)
                return render(request, 'SignUp.html', {'message': 'Username already exists.'})
            except User.DoesNotExist:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                email=email, password=f_pass)
                profile = UserProfile(user=user, phone=phone)
                profile.save()
                return render(request, 'SignUp.html', {'message': 'User Registered Successfully.'})
        return render(request, 'SignUp.html', {'message': "Passwords don't match"})


def signin(request):
    if request.method == 'GET':
        return render(request, 'SignIn.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return render(request, 'home.html', {'message': user})
        else:
            return render(request, 'SignIn.html', {'message': 'Invalid Credentials.'})


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return render(request, 'SignIn.html', {'message': 'You logged out Successfully.'})


def home(request):
    if request.method == 'POST':
        return render(request, 'SignIn.html')


def quiz(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    user = User.objects.get(username=username)
    if request.method == "GET":
        try:
            response_to_get = Response.objects.filter(user=user).last()
            global id1
            global ques
            global ques_list
            global ques_str
            list = response_to_get.question_attempted
            ques_list = list.split(" ")
            different = 0
            while (different == 0):
                id1 = random.randint(1, 10)
                if str(id1) not in ques_list:
                    different = 1
            ques = Question.objects.get(id=id1)
            ques_list.append(id1)
            ques_str = ' '.join(map(str, ques_list))
            current_score_to_show = response_to_get.current_score
            sr_no = response_to_get.no_question_solved + 1
            return render(request, 'quiz.html', {'question': ques, 'sr': sr_no, 'score': current_score_to_show})
        except AttributeError:
            id1 = random.randint(1, 10)
            ques = Question.objects.get(id=id1)
            ques_list = []
            ques_list.append(id1)
            ques_str = ' '.join(map(str, ques_list))
            sr_no = 1
            current_score_to_show = 0
            return render(request, 'quiz.html', {'question': ques, 'sr': sr_no, 'score':current_score_to_show})
    if request.method == 'POST':
        attempt_1 = request.POST.get('attempt1')
        attempt_2 = request.POST.get('attempt2')
        try:
            response_to_update = Response.objects.filter(user=user).last()
            no_question_solved_update = response_to_update.no_question_solved + 1
            if ((int(attempt_1) == ques.correct_ans) | (int(attempt_2) == ques.correct_ans)):
                global current_score_to_update
                current_score_to_update = response_to_update.current_score + 4
            else:
                current_score_to_update = response_to_update.current_score - 2
            response = Response(question=ques, user=user, attempt_1=attempt_1, attempt_2=attempt_2, no_question_solved=no_question_solved_update,
                                current_score = current_score_to_update, question_attempted = ques_str)
            response.save()
            if no_question_solved_update < 10:
                return redirect('quiz')
            elif no_question_solved_update >= 10:
                auth.logout(request)
                user1 = UserProfile.objects.get(user = user)
                user1.score = current_score_to_update
                user1.save(update_fields=["score"])
                return render(request, 'SignIn.html', {'message': 'Your responses have been recorded successfully.', 'score': current_score_to_update})
        except AttributeError:
            if ((int(attempt_1) == ques.correct_ans) | (int(attempt_2) == ques.correct_ans)):
                response = Response(question=ques, user=user, attempt_1=attempt_1, attempt_2=attempt_2,
                                    no_question_solved=1, current_score=4, question_attempted = ques_str)
                response.save()
                return redirect('quiz')
            else:
                response = Response(question=ques, user=user, attempt_1=attempt_1, attempt_2=attempt_2,
                                    no_question_solved=1, current_score=-2, question_attempted = ques_str)
                response.save()
                return redirect('quiz')
