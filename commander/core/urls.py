from django.contrib import admin
from django.urls import include, path  # add this
from src.utils.direct_method_constants import DeviceID

device_list = DeviceID.getDevices()

urlpatterns = [
    path("admin/", admin.site.urls),  # Django admin route
    path("", include("apps.authentication.urls")),  # Auth routes - login / register
    path("", include("apps.home.urls")),  # UI Kits Html files
    path("chat/", include("apps.chat.urls")),
] + [path(f"{device}/", include("apps.stingray.urls")) for device in device_list]
