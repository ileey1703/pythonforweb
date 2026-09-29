from django.db import models
from EntrepriseApp.models import Entreprise

# Create your models here.
class Expedition(models.Model):
    reference= models.CharField(max_length=50, unique=True)
    ville_depart=models.CharField(max_length=80)
    ville_arrive=models.CharField(max_length=80)
    poids_kg=models.DecimalField(max_digits=10,decimal_places=2)
    date_souhaitee=models.DateTimeField()
    description=models.TextField()
    statut=models.CharField(max_length=100,choices=[('en_attente','en_attente'),
    ('t','terminee'),
    ('a','annulee')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)
    entreprise =models.ForeignKey(Entreprise, on_delete=models.CASCADE,related_name='expeditions')


   