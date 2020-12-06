from django.shortcuts import render
from django.http import HttpResponse
from .statefunc import covidplotter

def COVIDstateanaly(request, state):
    covidplotter(state)
    print(state)
    return render(request,'covid/covid.html')
