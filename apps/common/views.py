from django.shortcuts import render
from apps.movies.models import Movie


def home_view(request):

    return render(request, 'index.html')


def about_view(request):
    return render(request,'about.html')


