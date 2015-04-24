from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse


def index(request):
    return redirect('new')

def new(request):
    return render(request, 'new.html')


def save(request):
    str_values = ""
    values =  request.POST.getlist('name[]')
    for value in values:
        str_values = str_values + ", " + value
    return HttpResponse("Values: " + str_values )
