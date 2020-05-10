from django.urls import path
from . import views

urlpatterns = [
    path('', views.version.as_view()),
]
