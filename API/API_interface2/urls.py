from django.urls import path, re_path
from . import views

urlpatterns = [
    path('login/', views.login.as_view()),
    path('query/classroom/', views.query_classroom.as_view()),
    path('query/dll/', views.query_ddl.as_view()),
]