from django.urls import path
from . import views

urlpatterns = [
    path('', views.QueryDdl.as_view()),
    path('Calendar/', views.QuerySchoolCalendar.as_view()),
]
