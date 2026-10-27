from datetime import timedelta

from django.contrib.admin import AdminSite
from django.db.models import Count
from django.template.response import TemplateResponse
from django.urls import path
from django.utils import timezone


class TransConnectAdminSite(AdminSite):
    site_header = "TransConnect - Administration"
    site_title = "TransConnect"
    index_title = "Tableau de bord TransConnect"
    index_template = "admin/transconnect_index.html"

    def get_urls(self):
        return [
            path(
                "health-check/",
                self.admin_view(self.health_check_view),
                name="health_check",
            ),
            *super().get_urls(),
        ]

    def health_check_view(self, request):
        from EntrepriseApp.models import Entreprise
        from ExpeditionApp.models import Expedition
        from OffreApp.models import offre
        from VehiculeApp.models import Vehicule

        seuil_expeditions = timezone.now() - timedelta(days=7)
        offres_incoherentes = offre.objects.filter(
            statut__in=("p", "a")
        ).exclude(expedition__statut__in=("publiee", "attribuee"))
        expeditions_bloquees = Expedition.objects.filter(
            statut="publiee",
            created_at__lt=seuil_expeditions,
        )
        transporteurs_sans_vehicule = (
            Entreprise.objects.filter(type_entreprise="t")
            .annotate(nombre_vehicules=Count("vehicules"))
            .filter(nombre_vehicules=0)
        )
        vehicules_disponibles_attribues = Vehicule.objects.filter(
            disponible=True,
            offres__statut="a",
        ).distinct()
        doublons_offres = (
            offre.objects.filter(statut="p")
            .values("entreprise__raison_social", "expedition__reference")
            .annotate(nombre=Count("pk"))
            .filter(nombre__gt=1)
            .order_by("expedition__reference", "entreprise__raison_social")
        )

        controles = [
            {
                "titre": "Offres incohérentes",
                "nombre": offres_incoherentes.count(),
                "elements": offres_incoherentes.select_related(
                    "entreprise", "expedition"
                )[:100],
            },
            {
                "titre": "Expéditions publiées depuis plus de 7 jours",
                "nombre": expeditions_bloquees.count(),
                "elements": expeditions_bloquees[:100],
            },
            {
                "titre": "Transporteurs sans véhicule",
                "nombre": transporteurs_sans_vehicule.count(),
                "elements": transporteurs_sans_vehicule[:100],
            },
            {
                "titre": "Véhicules disponibles malgré une offre acceptée",
                "nombre": vehicules_disponibles_attribues.count(),
                "elements": vehicules_disponibles_attribues[:100],
            },
            {
                "titre": "Doublons d'offres proposées",
                "nombre": doublons_offres.count(),
                "elements": doublons_offres[:100],
            },
        ]
        context = {
            **self.each_context(request),
            "title": "Contrôle d'intégrité",
            "controles": controles,
        }
        return TemplateResponse(request, "admin/health_check.html", context)


admin_site = TransConnectAdminSite(name="admin")
