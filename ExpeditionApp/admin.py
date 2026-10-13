from django.contrib import admin
from .models import Expedition


@admin.register(Expedition)
class ExpeditionAdmin(admin.ModelAdmin):
    list_display = (
        'reference',
        'ville_depart',
        'ville_arrive',
        'poids_kg',
        'statut',
        'entreprise',
        'date_souhaitee',
    )
    search_fields = (
        'reference',
        'ville_depart',
        'ville_arrive',
        'entreprise__raison_social',
    )
    list_filter = ('statut', 'entreprise')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Trajet', {
            'fields': ('reference', 'ville_depart', 'ville_arrive')
        }),
        ('Détails de l’expédition', {
            'fields': ('poids_kg', 'date_souhaitee', 'description')
        }),
        ('Statut et rattachement', {
            'fields': ('statut', 'entreprise')
        }),
        ('Horodatage', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
