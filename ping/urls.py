from django.urls import path
from . import views

urlpatterns = [
    path('', views.Ping.as_view())
]
