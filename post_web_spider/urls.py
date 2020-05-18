from django.urls import path
from . import views

urlpatterns = [
    path('delete/', views.DeleteStudent.as_view()),
    path('update/', views.UpdateTime.as_view()),
]
