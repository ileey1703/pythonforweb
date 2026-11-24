from django import forms
from django.template.backends import django

from .models import Entreprise, Utilisateur
from django.contrib.auth.forms import UserCreationForm


class EntrepriseForm(forms.ModelForm):
    class Meta:
        model = Entreprise
        exclude = ("created_at", "updated_at")

class registerUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Utilisateur
        fields = UserCreationForm.Meta.fields + ("email","role","telephone","last_name","first_name")

