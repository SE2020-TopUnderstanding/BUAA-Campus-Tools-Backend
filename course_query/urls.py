from django.urls import path
from . import views

urlpatterns = [
    path('', views.CourseList.as_view()),
    path('search/', views.Search.as_view()),
    path('evaluation/student/', views.CourseEvaluations.as_view()),
    path('evaluation/teacher/', views.TeacherEvaluations.as_view())
]
