from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_games, name="games"),
    path('all', views.all_games, name="all_games"),

    # Game CRUD
    path('create/', views.game_create, name="game_create"),
    path('<int:pk>/', views.game_detail, name='game_detail'),
    path('update/<int:pk>/', views.game_update, name='game_update'),
    path('obtain/', views.obtain_game, name='obtain_game'),

    # Console CRUD
    path('new_console/', views.console_platform_create, name='console_create'),
    path('console_update/<int:pk>/', views.console_platform_update, name='console_update'),

    # OwnedGame
    path('owned_games', views.owned_games_get, name="owned_games"),
    path('owned_game/update/<int:pk>/', views.owned_game_update, name="owned_game_update"),
]