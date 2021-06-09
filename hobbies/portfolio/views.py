from django.shortcuts import render, HttpResponse
import random

def index(request):
    colors = [
        '#3273dc',
        'orange',
        'purple',
        'blueviolet',
        'coral',
        'crimson',
        'deepskyblue',
        'indigo'
    ]
    return render(request, 'index.html', {'backgroundcolor': random.choice(colors)})