from django.urls import path
from . import views

urlpatterns = [
    path('', views.query_ddl.as_view()),
]
