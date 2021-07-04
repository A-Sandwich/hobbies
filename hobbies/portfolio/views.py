from django.shortcuts import render, HttpResponse
from random import choice, seed
from .helper import Helper
from .popomodels import POPOImage

def index(request):
    helper = Helper()
    primary_image = helper.select_static_file('primary')
    programming_image = helper.select_static_file('programming')
    food_image = helper.select_static_file('food')
    other_image = helper.select_static_file('other')
    color = helper.choose_css_color()

    return render(request, 'index.html', {
        'backgroundcolor': color,
        'primary_image': primary_image,
        'programming_image': programming_image,
        'food_image': food_image,
        'other_image': other_image
    })


