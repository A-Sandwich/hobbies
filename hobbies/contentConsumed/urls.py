from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('all/', views.all, name="all"),
    path('new/', views.new, name="new"),
    path('<int:game_id>/', views.detail, name='detail'),
]