from django import forms

from .models import offre


class OffreForm(forms.ModelForm):
    class Meta:
        model = offre
        exclude = ("created_at", "updated_at")
        widgets = {
            "date_proposition": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
