from django.db import models
from EntrepriseApp.models import Entreprise

# Create your models here.
class Vehicule(models.Model):
    immatriculation=models.CharField(max_length=50, unique=True)
    type_vehicule=models.CharField(max_length=100,choices=[('c','camionnette'),
    ('f','fourgon'),
    ('sr','semi-remorque'),
    ('cp','camion porteur')])
    capacite_kg=models.PositiveIntegerField()
    disponible=models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)
    entreprise =models.ForeignKey(Entreprise, on_delete=models.CASCADE,related_name='vehicules')