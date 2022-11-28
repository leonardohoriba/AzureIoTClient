from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.index),
    re_path(r"^.*stop_button.*$", views.stopButton),
    re_path(r"^.*start_button.*$", views.startButton),
]
