from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.query_ddl.as_view()),
]