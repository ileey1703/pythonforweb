from django.contrib import admin
from .models import offre


@admin.register(offre)
class OffreAdmin(admin.ModelAdmin):
    list_display = ('entreprise', 'expedition', 'vehicule', 'prix', 'delai_jours', 'statut')
    search_fields = (
        'entreprise__raison_social',
        'expedition__reference',
        'vehicule__immatriculation',
    )
    list_filter = ('statut', 'entreprise')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Rattachement', {
            'fields': ('entreprise', 'expedition', 'vehicule')
        }),
        ('Détails de l’offre', {
            'fields': ('prix', 'delai_jours', 'statut', 'date_proposition')
        }),
        ('Horodatage', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
