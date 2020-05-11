from django.urls import path
from . import views

urlpatterns = [
    path('', views.Version.as_view()),
]
