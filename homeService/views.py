from http.client import HTTPResponse

from django.shortcuts import render, redirect


# Create your views here.

def home_page(request):
    return redirect('login')
    return render(request, 'home/home.html')
