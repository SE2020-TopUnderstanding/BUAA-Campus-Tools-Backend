from django.urls import path
from . import views

urlpatterns = [
    path('', views.Login.as_view())
]
