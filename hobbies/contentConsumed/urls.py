from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_games, name="games"),
    path('all/', views.all_games, name="all_games"),
    path('new/', views.new_game, name="new_game"),
    path('<int:game_id>/', views.detail_game, name='detail_game'),
    path('obtain/', views.obtain_game, name='obtain_game'),
    path('new_console/', views.new_console_platform, name='new_console'),
]