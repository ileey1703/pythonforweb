from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import DeleteView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from .forms import ExpeditionForm
from django.urls import reverse_lazy
from .models import Expedition


# Create your views here.
def home(request):
    return render(request, "expedition/home.html")
def welcome(request , name):
    return render(request, "expedition/welcome.html", {"name": name})

def listExpedition(request):
    liste= Expedition.objects.filter(statut="publiee").order_by('date_souhaitee')
    return render(request, 'expedition/list.html',{"list":liste})
def detailExpedition(request, pk):
    expedition= Expedition.objects.get(pk=pk)
    return render(request, 'expedition/detail.html',{"expedition":expedition})
def deleteExpedition(request, pk):
    expedition= Expedition.objects.get(pk=pk)
    expedition.delete()
    return HttpResponse(f"expedition {pk} deleted")

class ListExpedition(ListView):
    model=Expedition
    template_name='expedition/list.html'
    context_object_name='list'

class DetailExpedition(DetailView):
    model=Expedition
    template_name='expedition/detail.html'
    context_object_name='expedition'
class DeleteExpedition(DeleteView):
    model=Expedition
    template_name='expedition/delete.html'
    success_url=reverse_lazy('listclass')

class CreateExpedition(CreateView):
    model=Expedition
    template_name='expedition/forms.html'
    #fields="__all__"
    form_class = ExpeditionForm
    success_url=reverse_lazy('listclass')

class UpdateExpedition(UpdateView):
    model=Expedition
    template_name='expedition/forms.html'
    form_class = ExpeditionForm
    success_url=reverse_lazy('listclass')