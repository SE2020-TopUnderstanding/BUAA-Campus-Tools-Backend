from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.ScoreList.as_view())
]