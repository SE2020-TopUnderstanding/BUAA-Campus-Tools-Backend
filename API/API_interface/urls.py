from django.urls import path, re_path
from . import views

urlpatterns = [
    path('<int:pk>', views.CourseList.as_view())
]