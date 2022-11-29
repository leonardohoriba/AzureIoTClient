from django.http import HttpResponse
from django.template import loader
from src.utils.direct_method_constants import DeviceID
from src.helpers.socket_client import SocketClient

device_list = DeviceID().getDevices()

def index(request):
    device_id = request.path.split("/")[1]
    context = {
        "segment": device_id,
        "devices": device_list,
        "device": device_id
    }

    html_template = loader.get_template("stingray/index.html")
    return HttpResponse(html_template.render(context, request))

def startButton(request):
    device_id = request.path.split("/")[1]
    context = {
        "segment": device_id,
        "devices": device_list,
        "device": device_id
    }
    
    socket_client = SocketClient()
    res = socket_client.send(msg={
        "start_button": True
    })

    html_template = loader.get_template("stingray/index.html")
    return HttpResponse(html_template.render(context, request))

def stopButton(request):
    device_id = request.path.split("/")[1]
    context = {
        "segment": device_id,
        "devices": device_list,
        "device": device_id
    }
    
    socket_client = SocketClient()
    res = socket_client.send(msg={
        "stop_button": True
    })

    html_template = loader.get_template("stingray/index.html")
    return HttpResponse(html_template.render(context, request))