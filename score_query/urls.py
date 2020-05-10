from django.urls import path
from . import views

urlpatterns = [
    path('', views.ScoreList.as_view()),
    path('gpa/', views.GPACalculate.as_view()),
    path('avg_score/', views.AvgScoreCalculate.as_view())
]
