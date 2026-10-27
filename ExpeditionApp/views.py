from django.shortcuts import render
from django.http import HttpResponse

from .models import Expedition


# Create your views here.
def home(request):
    return HttpResponse("<h1>Welcome To ..... </h1>")
def welcome(request , name):
    return HttpResponse(f"hello {name}")

def listExpedition(request):
    liste= Expedition.objects.filter(statut="publiee").order_by('date_souhaitee')
    return render(request, 'expedition/list.html',{"list":liste})
def detailExpedition(request, pk):
    expedition= Expedition.objects.get(pk=pk)
    return render(request, 'expedition/detail.html',{"expedition":expedition})
def deleteExpedition(request, pk):
    expedition= get_object_or_404(Expedition, pk=pk)
    expedition.delete()
    return HttpResponse(f"expedition {pk} deleted")