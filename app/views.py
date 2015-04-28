from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse


def index(request):
    return redirect('new_step1')

def new_step1(request):
    return render(request, 'new.html')

def new_step2(request):
    return render(request, 'new1.html')

def new_step3(request):
    return render(request, 'new2.html')

def new_step4(request):
    return render(request, 'new3.html')

def new_step5(request):
    return render(request, 'new4.html')


def save(request):
    str_values = ""
    values =  request.POST.getlist('name[]')
    for value in values:
        str_values = str_values + ", " + value
    return HttpResponse("Values: " + str_values )
