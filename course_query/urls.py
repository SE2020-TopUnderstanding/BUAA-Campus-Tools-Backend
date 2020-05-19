from django.urls import path
from . import views

urlpatterns = [
    path('', views.CourseList.as_view()),
    path('search/', views.Search.as_view()),
    path('evaluation/student/', views.CourseEvaluations.as_view()),
    path('evaluation/teacher/', views.TeacherEvaluations.as_view()),
    path('evaluation/student/up/', views.CourseEvaluationAction.as_view({'post': 'up_action'})),
    path('evaluation/student/cancel_up/', views.CourseEvaluationAction.as_view({'post': 'cancel_up_action'})),
    path('evaluation/student/down/', views.CourseEvaluationAction.as_view({'post': 'down_action'})),
    path('evaluation/student/cancel_down/', views.CourseEvaluationAction.as_view({'post': 'cancel_down_action'}))
]
