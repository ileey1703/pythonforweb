from django.contrib import admin
from .models import Vehicule
# Register your models here.
@admin.register(Vehicule)

class VehiculeAdmin(admin.ModelAdmin):
    list_display = ('type_vehicule','disponible','capacite_kg')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Identification', {
            'fields': ('immatriculation', 'type_vehicule','capacite_kg')
        }),
        ('Statut et rattachement', {
            'fields': ('disponible', 'entreprise')
        }),
        ('Horodatage', {
            'fields': ('created_at', 'updated_at'),
            #cacher les champs created_at et updated_at dans l'interface d'administration
            'classes': ('collapse',),
        }),
    )
    
#admin.site.register(Vehicule, VehiculeAdmin)
