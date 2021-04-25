from django.urls import path
from . import views

urlpatterns = [
    path('/', views.all, name="games"),
    path('all/', views.all, name="all"),
    path('new/', views.new, name="new"),
    path('<int:game_id>/', views.detail, name='detail'),
    path('obtain/', views.obtain, name='obtain'),
]