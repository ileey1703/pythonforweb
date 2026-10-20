from django.contrib import admin
from .models import Expedition
from django.utils import timezone


class EnRetardFilter(admin.SimpleListFilter):
    title="en retard"
    parameter_name = "en_retard"
    def lookups(self,request , model_admin):
        return [("oui", "Oui"),("non", "Non")]
    def queryset(self,request, queryset):
        aujourd_hui = timezone.now().date()
        if self.value() == "oui":
            return queryset.filter(statut="publiee", date_souhaitee__lt=aujourd_hui)
        if self.value() =="non":
            return queryset.exclude(statut="publiee", date_souhaitee__lt=aujourd_hui)
        return queryset 
    


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
    list_filter = ('statut', 'ville_depart','ville_arrive','date_souhaitee',EnRetardFilter,)
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
