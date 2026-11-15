from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import OffreForm
from .models import offre


class OffreList(ListView):
    model = offre
    template_name = "offre/list.html"
    context_object_name = "offres"


class OffreDetail(DetailView):
    model = offre
    template_name = "offre/detail.html"
    context_object_name = "offre"


class OffreCreate(CreateView):
    model = offre
    form_class = OffreForm
    template_name = "crud/form.html"
    success_url = reverse_lazy("offre_list")
    extra_context = {
        "page_title": "Nouvelle offre",
        "submit_label": "Créer l'offre",
        "list_url": "offre_list",
    }


class OffreUpdate(UpdateView):
    model = offre
    form_class = OffreForm
    template_name = "crud/form.html"
    success_url = reverse_lazy("offre_list")
    extra_context = {
        "page_title": "Modifier l'offre",
        "submit_label": "Enregistrer les modifications",
        "list_url": "offre_list",
    }


class OffreDelete(DeleteView):
    model = offre
    template_name = "crud/delete.html"
    success_url = reverse_lazy("offre_list")
    extra_context = {
        "page_title": "Supprimer cette offre ?",
        "list_url": "offre_list",
    }
