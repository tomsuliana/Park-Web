from askme.models import *
from askme.forms import  LoginForm, RegistrationForm, SettingsForm
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET
from django.http import Http404
from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import pdb
from django.urls import reverse


def paginate(objects, request, per_page=10):
    page_num = request.GET.get('page', default='1')
    p = Paginator(objects, per_page)

    if page_num.isdigit():
        page_num = int(page_num)
    else:
        page_num = 1

    if page_num > p.num_pages:
        page_num = p.num_pages
    elif page_num < 1:
        page_num = 1

    return p.page(page_num), str(page_num), list(map(str, p.get_elided_page_range(page_num, on_each_side=2)))


@require_GET
def index(request):
    questions, cur_page, pages = paginate(Question.objects.all().order_by('-id'), request)
    context = {
        'questions': questions,
        'pages': pages,
        'cur_page': cur_page
    }
    return render(request, 'index.html', context=context)


def question(request, question_id):
    if (question_id >= len(Question.objects.all()) + 4):
        raise Http404()

    answers, cur_page, pages = paginate(Answer.objects.filter(question=question_id), request, 3)

    context = {
        'question':  Question.objects.get(id=question_id),
        'answers': answers,
        'pages': pages,
        'cur_page': cur_page
        }
    return render(request, 'question.html', context)

@require_GET
def hot(request):
    questions, cur_page, pages = paginate(Question.objects.in_rating_order(), request)
    context = {
        'questions': questions,
        'pages': pages,
        'cur_page': cur_page
    }
    return render(request, 'hot.html', context=context)

@require_GET
def tag(request, tag_name):
    questions, cur_page, pages = paginate(Question.objects.by_tag(tag_name=tag_name), request)
    context = {
        'questions': questions,
        'pages': pages,
        'cur_page': cur_page,
        'tag_name': tag_name,
        }
    return render(request, 'tag.html', context=context)


def log_in(request):
    # us = User.objects.filter(username="uliana")
    # print(us[0].password)
    if request.method == "GET":
        login_form = LoginForm()
    elif request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(request=request, **login_form.cleaned_data)
            if user:
                login(request, user)
                return redirect(reverse(request.POST['continue_']))
            else:
                login_form.add_error(None, "Invalid username or password")
    return render(request, 'login.html', context={'form': login_form})

def logout_view(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER'))

def signup(request):
    if request.method == "GET":
        register_form = RegistrationForm()
    elif request.method == "POST":
        register_form = RegistrationForm(request.POST)
        if register_form.is_valid():
            us = new_user_(request.POST)
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                user = auth.authenticate(request=request, **login_form.cleaned_data)
                if user:
                    login(request, user)
                    return redirect(reverse('index'))

    return render(request, 'signup.html', context={'form': register_form})

@login_required
def ask(request):
    return render(request, 'ask.html')

@login_required
def settings(request):
    if request.method == "GET":
        set_form = SettingsForm()
    return render(request, 'settings.html', context={'form': set_form})



