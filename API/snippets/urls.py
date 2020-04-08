from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.snippet_list),
    path('<int:pk>', views.snippet_detail)
]