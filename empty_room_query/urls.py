from django.urls import path
from . import views

urlpatterns = [
    path('', views.query_classroom.as_view()),
]
