from django.db import models
from django.contrib.auth.models import AbstractUser 

# Create your models here.
class Utilisateur(AbstractUser):
    email=models.EmailField(unique=True)
    user_id =models.CharField(primery_key=True,max_lenght=8)
    telephone =models.CharField(max_lenght=15, blank=True ,null=True)
    role = models.CharField(max_lenght=20,choices=[
        ('admin','Admin'),
        ('c','chargeur'),
        ('t','transpporteur')
    ],default='c')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)




class Entreprise(models.Model):
    raison_social = models.CharField(max_length=200, blank=False ,null=False)
    matricule_fiscal =models.CharField(max_length=17 ,unique=True)
    adresse = models.TextField()
    type_entreprise=models.CharField(max_length=100,choices=[('c','chargeur'),
    ('t','transporteur')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)
    gerant= models.OneToOneField(Utilisateur ,on_delete=models.CASCADE,related_name='entreprise')
    