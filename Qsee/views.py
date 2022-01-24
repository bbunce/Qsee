from django.http import HttpResponse, Http404, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, render, get_list_or_404
from django.template import loader
from .models import Assay

# Create your views here.
def index(request):
    try:
        assays = Assay.objects.all()
    except Assay.DoesNotExist:
        raise Http404("Assay does not exist")
    return render(request, 'Qsee/index.html', {'list_assay': assays})

def assays(request, id):
    return HttpResponse(f"Qsee assays {id}")

def controls(request):
    return HttpResponse("Qsee controls")

def analysers(request):
    return HttpResponse("Qsee analysers")

def tests(request, control_id):
    return HttpResponse(f"Qsee results for {control_id}")

