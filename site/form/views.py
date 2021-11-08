from django.shortcuts import render
import django.http as http

def index(request):
    return http.HttpResponse("Hello world.")

def data(request):
    return http.JsonResponse({"x": 3, "y": 4})
