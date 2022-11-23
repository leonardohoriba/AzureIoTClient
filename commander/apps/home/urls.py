from django.urls import include, path, re_path

from apps.home import views

urlpatterns = [
    # The home page
    path("", views.index, name="home"),
    path("chat/", include("apps.chat.urls"), name="chat"),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),
]
