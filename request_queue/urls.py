from django.urls import path
from . import views

urlpatterns = [
    path('', views.Queue.as_view()),
    path('', views.AddCourseRequest.as_view()),
    path('add_course/', views.AddCourseRequest.as_view()),
    path('score_course/', views.ScoreOrCourseRequest.as_view()),
    path('ddl/', views.DDLRequest.as_view()),
]
