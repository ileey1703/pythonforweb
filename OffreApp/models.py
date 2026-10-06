from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from EntrepriseApp.models import Entreprise
from VehiculeApp.models import Vehicule
from ExpeditionApp.models import Expedition


class offre(models.Model):
    prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.1'))]
    )
    delai_jours = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    statut=models.CharField(max_length=100,choices=[('p','proposee'),
    ('a','acceptee'),
    ('r','refusee'),
    ('re','retiree')], default='p')
    date_proposition=models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)
    entreprise =models.ForeignKey(Entreprise, on_delete=models.CASCADE,related_name='offres')
    expedition =models.ForeignKey(Expedition, on_delete=models.CASCADE,related_name='offres')
    vehicule=models.ForeignKey(Vehicule, on_delete=models.CASCADE,related_name='offres')
