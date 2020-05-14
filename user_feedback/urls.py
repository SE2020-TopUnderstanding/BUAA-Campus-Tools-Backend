from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserFeedback.as_view())
]
