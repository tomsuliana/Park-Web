from . import models
from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET
from django.http import Http404


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
    questions, cur_page, pages = paginate(models.QUESTIONS, request)
    context = {
        'questions': questions,
        'pages': pages,
        'cur_page': cur_page
    }
    return render(request, 'index.html', context=context)


def question(request, question_id):
    if (question_id >= len(models.QUESTIONS)):
        raise Http404()

    answers, cur_page, pages = paginate(models.ANSWERS, request, 3)

    context = {
        'question': models.QUESTIONS[question_id],
        'answers': answers,
        'pages': pages,
        'cur_page': cur_page
        }
    return render(request, 'question.html', context)

@require_GET
def hot(request):
    questions, cur_page, pages = paginate(models.QUESTIONS, request)
    context = {
        'questions': questions,
        'pages': pages,
        'cur_page': cur_page
    }
    return render(request, 'hot.html', context=context)

@require_GET
def tag(request, tag_name):
    questions, cur_page, pages = paginate(models.QUESTIONS, request)
    context = {
        'questions': questions,
        'pages': pages,
        'cur_page': cur_page,
        'tag_name': tag_name,
        }
    return render(request, 'tag.html', context=context)


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def ask(request):
    return render(request, 'ask.html')


def settings(request):
    return render(request, 'settings.html')



