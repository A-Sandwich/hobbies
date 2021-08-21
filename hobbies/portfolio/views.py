from django.shortcuts import render, HttpResponse
from random import choice, seed
from .helper import Helper
from .popomodels import POPOImage
from stats.models import ExerciseTotal
from datetime import date

def index(request):
    helper = Helper()
    primary_image = helper.select_static_file('primary')
    programming_image = helper.select_static_file('programming')
    food_image = helper.select_static_file('food')
    other_image = helper.select_static_file('other')
    color = helper.choose_css_color()
    running_exercise = ExerciseTotal.objects.filter(year=str(date.today().year), exercise_type="running").first()
    distance = 0
    if running_exercise:
        distance = running_exercise.get_miles()

    return render(request, 'index.html', {
        'backgroundcolor': color,
        'primary_image': primary_image,
        'programming_image': programming_image,
        'food_image': food_image,
        'other_image': other_image,
        'distance': round(distance, 1)
    })


