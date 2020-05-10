from django.urls import path
from . import views

urlpatterns = [
    path('', views.TestList.as_view())
]
