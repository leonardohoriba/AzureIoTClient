from django.urls import include, path, re_path

from apps.home import views
from src.utils.direct_method_constants import DeviceID

device_list = DeviceID.getDevices()

urlpatterns = [
    # The home page
    path("", views.index, name="home"),
    re_path(r"^.*stop_button.*$", views.stopButton, name="stop_button"),
    re_path(r"^.*start_button.*$", views.startButton, name="start_button"),
    # path("chat/", include("apps.chat.urls"), name="chat"),
    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),
] + [path(f"{device}/", include("apps.stingray.urls"), name=device) for device in device_list]
