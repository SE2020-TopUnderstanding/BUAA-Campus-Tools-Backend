from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.delete_student.as_view()),
]