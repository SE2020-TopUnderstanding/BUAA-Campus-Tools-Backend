from django.urls import path
from . import views

urlpatterns = [
    path('', views.delete_student.as_view()),
]
