from django.urls import path
from . import views

urlpatterns = [
    path('', views.all, name="index"), # making this go to the all view for now
    path('all/', views.all, name="all"),
    path('new/', views.new, name="new"),
    path('<int:game_id>/', views.detail, name='detail'),
]