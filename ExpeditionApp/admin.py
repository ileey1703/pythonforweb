from django.contrib import admin
from .models import Expedition
from OffreApp.models import offre
from config.admin import admin_site
from django.utils import timezone


class OffreInline(admin.StackedInline):
    model = offre
    fk_name = 'expedition'
    fields = ('entreprise', 'vehicule', 'prix', 'delai_jours', 'statut', 'date_proposition')
    readonly_fields = fields
    extra = 0
    can_delete = False
    show_change_link = True

    def has_add_permission(self, request, obj=None):
        return False


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
    


@admin.register(Expedition, site=admin_site)
class ExpeditionAdmin(admin.ModelAdmin):
    inlines = [OffreInline]
    actions = ['cloturer_expeditions']
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

    @admin.action(description="Clôturer les expéditions sélectionnées")
    def cloturer_expeditions(self, request, queryset):
        expeditions_a_cloturer = queryset.filter(statut='attribuee')
        nombre_selectionne = queryset.count()
        nombre_cloturees = 0

        for expedition in expeditions_a_cloturer:
            expedition.statut = 'terminee'
            expedition.save()
            nombre_cloturees += 1

        nombre_ignorees = nombre_selectionne - nombre_cloturees
        self.message_user(
            request,
            f"{nombre_cloturees} expédition(s) clôturée(s). "
            f"{nombre_ignorees} expédition(s) ignorée(s) car elles ne sont pas en cours."
        )
