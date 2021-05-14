from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_games, name="games"),
    path('all/', views.all_games, name="all_games"),
    path('new/', views.game_create, name="game_create"),
    path('<int:game_id>/', views.detail_game, name='detail_game'),
    path('obtain/', views.obtain_game, name='obtain_game'),
    path('new_console/', views.console_platform_create, name='console_create'),
    path('console_update/<int:pk>/', views.console_platform_update, name='console_update'),
]