from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from src.utils.direct_method_constants import DeviceID


device_list = DeviceID.getDevices()

# @login_required(login_url="/login/")
def index(request):
    context = {"segment": device_list[0]}
    context["devices"] = DeviceID.getDevices()

    html_template = loader.get_template("stingray/index.html")
    return HttpResponse(html_template.render(context, request))
# def index(request):
#     context = {"segment": "index"}
#     context["devices"] = DeviceID.getDevices()

#     html_template = loader.get_template("home/index.html")
#     return HttpResponse(html_template.render(context, request))

# @login_required(login_url="/login/")
def stingray(request):
    context = {"segment": "stingray"}
    context["devices"] = DeviceID.getDevices()

    html_template = loader.get_template("home/stingray.html")
    return HttpResponse(html_template.render(context, request))

# @login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split("/")[-1]

        context["segment"] = load_template
        context["devices"] = DeviceID.getDevices()

        if load_template == "admin":
            return HttpResponseRedirect(reverse("admin:index"))
        elif load_template in device_list:
            html_template = loader.get_template(load_template)
            return HttpResponse(html_template.render(context, request))


        html_template = loader.get_template("home/" + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template("home/page-404.html")
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template("home/page-500.html")
        return HttpResponse(html_template.render(context, request))
