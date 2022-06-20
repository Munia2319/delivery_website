from django.urls import path
from . import views
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from delivery import views
from django.urls import include, path
from rest_framework import routers


app_name='delivery'

urlpatterns = [
    path('', views.home_page, name="home_page"),
    path('second/',views.second_page, name='second_page' ),
    path('third/',views.third_page, name='third' ),
    path('test/',views.test_page, name='test' ),
    path('api_view/',views.api_view),
    

    

    ]