# from django.http import HttpResponse

# def home(request):
#     return HttpResponse("Welcome to TeamFlow Backend API 🚀")

from django.shortcuts import render

def home(request):
    return render(request, "login.html")

def login_page(request):
    return render(request, "login.html")

def register_page(request):
    return render(request, "register.html")

def landing_page(request):
    return render(request, "landing.html")

def workspace_page(request):
    return render(request, "workspace.html")
