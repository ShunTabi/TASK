"""task URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path,include
from . import views

urlpatterns = [
    path("",views.index),
    path("classificationInsert",views.classificationInsert),
    path("classificationSelect/<int:num>",views.classificationSelect),
    path("classificationNameSelect",views.classificationNameSelect),
    path("taskInsert",views.taskInsert),
    path("taskSelect/<int:num>",views.taskSelect),
    path("taskNameSelect/<int:num>",views.taskNameSelect),
    path("taskNameSelect2",views.taskNameSelect2),
    path("activityInsert/<int:num>",views.activityInsert),
    path("activitySelect1",views.activitySelect1),
    path("activitySelect2/<int:num>",views.activitySelect2),
]
