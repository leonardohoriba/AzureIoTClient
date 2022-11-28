from django.http import HttpResponse
from django.template import loader
from src.utils.direct_method_constants import DeviceID


device_list = DeviceID.getDevices()

def index(request):
    device_id = request.path.split("/")[1]
    context = {
        "segment": device_id,
        "devices": device_list,
        "device": device_id
    }

    html_template = loader.get_template("stingray/index.html")
    return HttpResponse(html_template.render(context, request))
