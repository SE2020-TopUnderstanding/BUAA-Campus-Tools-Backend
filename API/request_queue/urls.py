from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.Queue.as_view()),
    path('timetable/', views.CourseRequest.as_view()),
    path('score/', views.ScoreRequest.as_view()),
    path('empty_room/', views.RoomRequest.as_view()),
    path('ddl/', views.DDLRequest.as_view()),
]