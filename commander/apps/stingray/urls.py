from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("start_button/", views.startButton),
    path("stop_button/", views.startButton),
]
