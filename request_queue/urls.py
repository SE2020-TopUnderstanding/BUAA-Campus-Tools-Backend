from django.urls import path
from . import views

urlpatterns = [
    path('', views.Queue.as_view()),
    path('', views.AddCourseRequest.as_view()),
    path('timetable/', views.CourseRequest.as_view()),
    path('score/', views.ScoreRequest.as_view()),
    path('ddl/', views.DDLRequest.as_view()),
]
