from django.urls import include, path, re_path

from apps.home import views
from src.utils.direct_method_constants import DeviceID

device_list = DeviceID.getDevices()

urlpatterns = [
    # The home page
    path("", views.index, name="home"),
    path("start_button", views.index, name="start_button"),
    path("stop_button", views.index, name="stop_button"),
    # path("chat/", include("apps.chat.urls"), name="chat"),
    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),
] + [path(f"{device}/", include("apps.stingray.urls"), name=device) for device in device_list]
