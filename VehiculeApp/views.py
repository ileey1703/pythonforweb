from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import VehiculeForm
from .models import Vehicule


class VehiculeList(ListView):
    model = Vehicule
    template_name = "vehicule/list.html"
    context_object_name = "vehicules"


class VehiculeDetail(DetailView):
    model = Vehicule
    template_name = "vehicule/detail.html"
    context_object_name = "vehicule"


class VehiculeCreate(CreateView):
    model = Vehicule
    form_class = VehiculeForm
    template_name = "crud/form.html"
    success_url = reverse_lazy("vehicule_list")
    extra_context = {
        "page_title": "Nouveau véhicule",
        "submit_label": "Créer le véhicule",
        "list_url": "vehicule_list",
    }


class VehiculeUpdate(UpdateView):
    model = Vehicule
    form_class = VehiculeForm
    template_name = "crud/form.html"
    success_url = reverse_lazy("vehicule_list")
    extra_context = {
        "page_title": "Modifier le véhicule",
        "submit_label": "Enregistrer les modifications",
        "list_url": "vehicule_list",
    }


class VehiculeDelete(DeleteView):
    model = Vehicule
    template_name = "crud/delete.html"
    success_url = reverse_lazy("vehicule_list")
    extra_context = {
        "page_title": "Supprimer ce véhicule ?",
        "list_url": "vehicule_list",
    }
