import csv
from io import StringIO

from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils import timezone

from EntrepriseApp.models import Entreprise, Utilisateur
from ExpeditionApp.models import Expedition
from VehiculeApp.models import Vehicule
from .admin import OffreAdmin
from .models import offre


class OffreAdminAndAcceptanceTests(TestCase):
    def create_entreprise(self, suffix, type_entreprise):
        utilisateur = Utilisateur.objects.create_user(
            username=f"utilisateur{suffix}",
            email=f"utilisateur{suffix}@gmail.com",
            password="test-password",
        )
        return Entreprise.objects.create(
            raison_social=f"Entreprise {suffix}",
            matricule_fiscal=f"1234567A{suffix}M001",
            adresse="12 rue de test, adresse suffisamment longue",
            type_entreprise=type_entreprise,
            gerant=utilisateur,
        )

    def setUp(self):
        self.chargeur = self.create_entreprise("B", "c")
        self.transporteur_1 = self.create_entreprise("C", "t")
        self.transporteur_2 = self.create_entreprise("D", "t")
        self.expedition = Expedition.objects.create(
            reference="EXP-TEST-00001",
            ville_depart="Paris",
            ville_arrive="Lyon",
            poids_kg=100,
            date_souhaitee=timezone.now(),
            description="Expédition de test",
            statut="publiee",
            entreprise=self.chargeur,
        )
        self.vehicule_1 = Vehicule.objects.create(
            immatriculation="TEST-C-001",
            type_vehicule="camionnette",
            capacite_kg=1000,
            disponible=True,
            entreprise=self.transporteur_1,
        )
        self.vehicule_2 = Vehicule.objects.create(
            immatriculation="TEST-D-001",
            type_vehicule="camionnette",
            capacite_kg=1000,
            disponible=True,
            entreprise=self.transporteur_2,
        )
        self.offre_acceptee = offre.objects.create(
            prix="100.00",
            delai_jours=3,
            statut="p",
            date_proposition=timezone.now(),
            entreprise=self.transporteur_1,
            expedition=self.expedition,
            vehicule=self.vehicule_1,
        )
        self.offre_refusee = offre.objects.create(
            prix="120.00",
            delai_jours=4,
            statut="p",
            date_proposition=timezone.now(),
            entreprise=self.transporteur_2,
            expedition=self.expedition,
            vehicule=self.vehicule_2,
        )

    def test_accepting_offer_updates_expedition_and_refuses_other_offers(self):
        self.offre_acceptee.statut = "a"
        self.offre_acceptee.full_clean()
        self.offre_acceptee.save()

        self.expedition.refresh_from_db()
        self.offre_refusee.refresh_from_db()
        self.assertEqual(self.expedition.statut, "attribuee")
        self.assertEqual(self.offre_refusee.statut, "r")

    def test_csv_export_and_integrity_page_are_available(self):
        request = RequestFactory().get("/admin/offres/")
        response = OffreAdmin(offre, AdminSite()).exporter_offres_csv(
            request,
            offre.objects.filter(pk=self.offre_acceptee.pk),
        )
        rows = list(csv.reader(StringIO(response.content.decode("utf-8"))))
        self.assertEqual(rows[0], ["reference_expedition", "transporteur", "prix", "statut"])
        self.assertEqual(rows[1][0], self.expedition.reference)

        staff_user = Utilisateur.objects.create_user(
            username="admin",
            email="admin@gmail.com",
            password="test-password",
            is_staff=True,
        )
        self.client.force_login(staff_user)
        health_check = self.client.get(reverse("admin:health_check"))
        self.assertEqual(health_check.status_code, 200)
        self.assertContains(health_check, "Contrôle d'intégrité des données")
        self.assertContains(health_check, "Doublons d&#x27;offres proposées")

        admin_index = self.client.get(reverse("admin:index"))
        self.assertEqual(admin_index.status_code, 200)
        self.assertContains(admin_index, "Ouvrir le contrôle d'intégrité")
