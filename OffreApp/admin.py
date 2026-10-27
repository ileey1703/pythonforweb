import csv

from django.contrib import admin
from django.http import HttpResponse

from config.admin import admin_site
from .models import offre


class PrixFilter(admin.SimpleListFilter):
    title="prix"
    parameter_name = "prix"
    def lookups(self,request , model_admin):
        return [("moins_100", "moins de 100"),("100_1000", "de 100 a 1000"),("1000_10000", "de 1000 a 10000")]
    def queryset(self,request, queryset):
        if self.value() == "moins_100":
            return queryset.filter( prix__lt=100)
        if self.value() =="100_1000":
            return queryset.filter( prix__gte=100, prix__lt=1000)
        if self.value() =="1000_10000":
            return queryset.filter( prix__gte=1000, prix__lt=10000)
        return queryset 
@admin.register(offre, site=admin_site)
class OffreAdmin(admin.ModelAdmin):
    actions = ("exporter_offres_csv",)
    list_display = ('entreprise', 'expedition', 'vehicule', 'prix', 'delai_jours', 'statut')
    search_fields = (
        'entreprise__raison_social',
        'expedition__reference',
        'vehicule__immatriculation',
    )
    list_filter = ('statut', 'entreprise',PrixFilter,)
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

    @admin.action(description="Exporter la sélection en CSV")
    def exporter_offres_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = 'attachment; filename="offres.csv"'
        writer = csv.writer(response)
        writer.writerow(
            ("reference_expedition", "transporteur", "prix", "statut")
        )
        for offre_selectionnee in queryset.select_related("expedition", "entreprise"):
            writer.writerow(
                (
                    offre_selectionnee.expedition.reference,
                    offre_selectionnee.entreprise.raison_social,
                    offre_selectionnee.prix,
                    offre_selectionnee.get_statut_display(),
                )
            )
        return response
