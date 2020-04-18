"""API URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('timetable/', include('course_query.urls')),
    path('classroom/', include('empty_room_query.urls')),
    path('ddl/', include('ddl_query.urls')),
    path('score/', include('score_query.urls')),
    path('tests/', include('tests_query.urls')),
    path('login/', include('user_login.urls')),
    path('ping/', include('ping.urls')),
]
