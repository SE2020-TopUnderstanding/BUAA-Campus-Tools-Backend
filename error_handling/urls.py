from django.urls import path
from . import views

urlpatterns = [
    path('', views.DeleteStudent.as_view()),
]
