from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
# Create your views here.
def home(request: HttpRequest):
    return render(request, 'home.html')