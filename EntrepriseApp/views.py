from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import EntrepriseForm
from .models import Entreprise


class EntrepriseList(ListView):
    model = Entreprise
    template_name = "entreprise/list.html"
    context_object_name = "entreprises"


class EntrepriseDetail(DetailView):
    model = Entreprise
    template_name = "entreprise/detail.html"
    context_object_name = "entreprise"


class EntrepriseCreate(CreateView):
    model = Entreprise
    form_class = EntrepriseForm
    template_name = "crud/form.html"
    success_url = reverse_lazy("entreprise_list")
    extra_context = {
        "page_title": "Nouvelle entreprise",
        "submit_label": "Créer l'entreprise",
        "list_url": "entreprise_list",
    }


class EntrepriseUpdate(UpdateView):
    model = Entreprise
    form_class = EntrepriseForm
    template_name = "crud/form.html"
    success_url = reverse_lazy("entreprise_list")
    extra_context = {
        "page_title": "Modifier l'entreprise",
        "submit_label": "Enregistrer les modifications",
        "list_url": "entreprise_list",
    }


class EntrepriseDelete(DeleteView):
    model = Entreprise
    template_name = "crud/delete.html"
    success_url = reverse_lazy("entreprise_list")
    extra_context = {
        "page_title": "Supprimer cette entreprise ?",
        "list_url": "entreprise_list",
    }
