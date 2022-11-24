from django.http import HttpResponse
from django.template import loader
from src.utils.direct_method_constants import DeviceID


device_list = DeviceID.getDevices()

def index(request):
    context = {
        "segment": "index",
        "devices": device_list,
        "device": request.path.split("/")[1]
    }

    html_template = loader.get_template("stingray/index.html")
    return HttpResponse(html_template.render(context, request))
