
import random

from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse

from utils.mongodb_conn import mongodb_car_info


def index(request):
    """网站首页"""
    cars = mongodb_car_info
    count = cars.find().count()
    car_list = [car for car in cars.find().limit(100)]
    car_list = random.sample(car_list, 27)
    context = {
        'count': count,
        'car_list': car_list,
    }
    return render(request, 'renrenche/index.html', context=context)


def index1(request):
    return render(request, 'renrenche/about-us.html')


def index2(request):
    return render(request, 'renrenche/blog-details.html')


def index3(request):
    return render(request, 'renrenche/class-details.html')


def index4(request):
    return render(request, 'renrenche/event.html')


def index5(request):
    return render(request, 'renrenche/shortcode.html')


def index6(request):
    return render(request, 'renrenche/teacher.html')
